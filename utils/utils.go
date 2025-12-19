package utils

import (
	"bytes"
	"encoding/base64"
	"encoding/csv"
	"encoding/gob"
	"encoding/hex"
	"errors"
	"fmt"
	"github.com/consensys/gnark-crypto/ecc/bn254/fr"
	"github.com/consensys/gnark-crypto/ecc/bn254/fr/poseidon"
	"github.com/shopspring/decimal"
	"hash"
	"io/ioutil"
	"math/big"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"time"
)

func ConvertAssetInfoToBytes(value any) []byte {
	switch t := value.(type) {
	case CexAssetInfo:
		equityBigInt := new(big.Int).SetUint64(t.TotalEquity)
		debtBigInt := new(big.Int).SetUint64(t.TotalDebt)
		basePriceBigInt := new(big.Int).SetUint64(t.BasePrice)
		return new(big.Int).Add(new(big.Int).Add(
			new(big.Int).Mul(equityBigInt, Uint64MaxValueBigIntSquare),
			new(big.Int).Mul(debtBigInt, Uint64MaxValueBigInt)),
			basePriceBigInt).Bytes()
	default:
		panic("not supported type")
	}
}

func SelectAssetValue(expectAssetIndex int, flag int, currentAssetPosition int, assets []AccountAsset) (*big.Int, bool) {
	if currentAssetPosition >= len(assets) {
		return ZeroBigInt, false
	}
	if int(assets[currentAssetPosition].Index) > expectAssetIndex {
		return ZeroBigInt, false
	} else {
		if flag == 1 {
			return new(big.Int).SetUint64(assets[currentAssetPosition].Debt), true
		} else {
			return new(big.Int).SetUint64(assets[currentAssetPosition].Equity), false
		}
	}
}

func ComputeUserAssetsCommitment(hasher *hash.Hash, assets []AccountAsset) []byte {
	(*hasher).Reset()
	nEles := (AssetCounts*2 + 2) / 3
	currentAssetPosition := 0
	for i := 0; i < nEles; i++ {
		expectAssetIndex := (3 * i) / 2
		flag := (3 * i) % 2
		aBigInt, positionChange := SelectAssetValue(expectAssetIndex, flag, currentAssetPosition, assets)
		if positionChange {
			currentAssetPosition += 1
		}

		expectAssetIndex = ((3 * i) + 1) / 2
		flag = ((3 * i) + 1) % 2
		bBigInt, positionChange := SelectAssetValue(expectAssetIndex, flag, currentAssetPosition, assets)
		if positionChange {
			currentAssetPosition += 1
		}

		expectAssetIndex = ((3 * i) + 2) / 2
		flag = ((3 * i) + 2) % 2
		cBigInt, positionChange := SelectAssetValue(expectAssetIndex, flag, currentAssetPosition, assets)
		if positionChange {
			currentAssetPosition += 1
		}

		sumBigIntBytes := new(big.Int).Add(new(big.Int).Add(
			new(big.Int).Mul(aBigInt, Uint64MaxValueBigIntSquare),
			new(big.Int).Mul(bBigInt, Uint64MaxValueBigInt)),
			cBigInt).Bytes()
		(*hasher).Write(sumBigIntBytes)
	}

	return (*hasher).Sum(nil)
}

func ReadUserAssets(dirname string) ([]AccountInfo, []CexAssetInfo, error) {
	userFiles, err := ioutil.ReadDir(dirname)
	if err != nil {
		return nil, nil, err
	}
	var accountInfo []AccountInfo
	var cexAssetInfo []CexAssetInfo

	workersNum := 8
	userFileNames := make([]string, 0)

	type UserParseRes struct {
		accounts []AccountInfo
		cex      []CexAssetInfo
		index    int
	}
	results := make([]chan UserParseRes, workersNum)
	for i := 0; i < workersNum; i++ {
		results[i] = make(chan UserParseRes, 1)
	}
	for _, userFile := range userFiles {
		if strings.Index(userFile.Name(), ".csv") == -1 {
			continue
		}
		userFileNames = append(userFileNames, filepath.Join(dirname, userFile.Name()))
	}
	for i := 0; i < workersNum; i++ {
		go func(workerId int) {
			for j := workerId; j < len(userFileNames); j += workersNum {
				if j >= len(userFileNames) {
					break
				}
				tmpAccountInfo, tmpCexAssetInfo, err := ReadUserDataFromCsvFile(userFileNames[j])
				if err != nil {
					panic(err.Error())
				}
				results[workerId] <- UserParseRes{
					accounts: tmpAccountInfo,
					cex:      tmpCexAssetInfo,
				}
			}
		}(i)
	}

	gcQuitChan := make(chan bool)
	go func() {
		for {
			select {
			case <-time.After(time.Second * 10):
				runtime.GC()
			case <-gcQuitChan:
				return
			}
		}
	}()

	quit := make(chan bool)
	go func() {
		for i := 0; i < len(userFileNames); i++ {
			res := <-results[i%workersNum]
			if i != 0 {
				for j := 0; j < len(res.accounts); j++ {
					res.accounts[j].AccountIndex += uint32(len(accountInfo))
				}
			}
			accountInfo = append(accountInfo, res.accounts...)
			if len(cexAssetInfo) == 0 {
				cexAssetInfo = res.cex
			}
		}
		quit <- true
	}()
	<-quit
	gcQuitChan <- true
	return accountInfo, cexAssetInfo, nil
}

func SafeAdd(a uint64, b uint64) (c uint64) {
	c = a + b
	if c < a {
		panic("overflow for balance")
	}
	return c
}

func ReadUserDataFromCsvFile(name string) ([]AccountInfo, []CexAssetInfo, error) {
	f, err := os.Open(name)
	if err != nil {
		return nil, nil, err
	}
	defer f.Close()
	csvReader := csv.NewReader(f)
	data, err := csvReader.ReadAll()
	accountIndex := 0
	cexAssetsInfo := make([]CexAssetInfo, AssetCounts)
	accounts := make([]AccountInfo, len(data)-1)
	assetCounts := (len(data[0]) - 3) / 4
	symbols := data[0]
	data = data[1:]
	for i := 0; i < assetCounts; i++ {
		cexAssetsInfo[i].Symbol = symbols[i*3+4]
		cexAssetsInfo[i].Index = uint32(i)
		multiplier := int64(100000000)
		if AssetTypeForTwoDigits[cexAssetsInfo[i].Symbol] {
			multiplier = 100000000000000
		}

		//for _, v := range data {
		//	basePrice, err := ConvertFloatStrToUint64(v[assetCounts*3+i+2], multiplier)
		//	if err != nil {
		//		fmt.Println("asset data wrong:", v[assetCounts*3+i+2], err.Error())
		//		continue
		//	}
		//	cexAssetsInfo[i].BasePrice = cexAssetsInfo[i].BasePrice + basePrice
		//
		//}

		cexAssetsInfo[i].BasePrice, err = ConvertFloatStrToUint64(data[0][assetCounts*3+i+2], multiplier)
		if err != nil {
			fmt.Println("asset data wrong:", data[0][assetCounts*3+i+2], err.Error())
			continue
		}

		//cexAssetsInfo[i].BasePrice, err = ConvertFloatStrToUint64(data[0][assetCounts*3+i+2], multiplier)
		//if err != nil {
		//	fmt.Println("asset data wrong:", data[0][assetCounts*3+i+2], err.Error())
		//	continue
		//}
		// fmt.Println("base price:", cexAssetsInfo[i].BasePrice)
	}

	invalidCounts := 0
	for i := 0; i < len(data); i++ {
		var account AccountInfo
		assets := make([]AccountAsset, 0, 8)
		account.TotalEquity = new(big.Int).SetInt64(0)
		account.TotalDebt = new(big.Int).SetInt64(0)
		// first element of data[i] is ID. we use accountIndex instead
		account.AccountIndex = uint32(accountIndex)
		accountId, err := hex.DecodeString(data[i][1])
		if err != nil || len(accountId) != 32 {
			panic("accountId is invalid: " + data[i][1])
		}
		account.AccountId = new(fr.Element).SetBytes(accountId).Marshal()
		var tmpAsset AccountAsset
		for j := 0; j < assetCounts; j++ {
			multiplier := int64(100000000)
			if AssetTypeForTwoDigits[cexAssetsInfo[j].Symbol] {
				multiplier = 100
			}
			equity, err := ConvertFloatStrToUint64(data[i][j*3+2], multiplier)
			if err != nil {
				fmt.Println(cexAssetsInfo)
				fmt.Println("the symbol is ", cexAssetsInfo[j].Symbol)
				fmt.Println("account", data[i][1], "equity data wrong:", err.Error())
				invalidCounts += 1
				continue
			}

			debt, err := ConvertFloatStrToUint64(data[i][j*3+3], multiplier)
			if err != nil {
				fmt.Println("the debt symbol is ", cexAssetsInfo[j].Symbol)
				fmt.Println("account", data[i][1], "debt data wrong:", err.Error())
				invalidCounts += 1
				continue
			}
			if equity != 0 || debt != 0 {
				tmpAsset.Index = uint16(j)
				tmpAsset.Equity = equity
				tmpAsset.Debt = debt
				assets = append(assets, tmpAsset)

				account.TotalEquity = new(big.Int).Add(account.TotalEquity,
					new(big.Int).Mul(new(big.Int).SetUint64(tmpAsset.Equity), new(big.Int).SetUint64(cexAssetsInfo[j].BasePrice)))
				account.TotalDebt = new(big.Int).Add(account.TotalDebt,
					new(big.Int).Mul(new(big.Int).SetUint64(tmpAsset.Debt), new(big.Int).SetUint64(cexAssetsInfo[j].BasePrice)))
			}
		}

		account.Assets = assets
		if account.TotalEquity.Cmp(account.TotalDebt) >= 0 {
			accounts[accountIndex] = account
			accountIndex += 1
		} else {
			invalidCounts += 1
			fmt.Println("account", data[i][1], "data wrong: total debt is bigger than equity:", account.TotalDebt, account.TotalEquity)
		}
		if i%100000 == 0 {
			runtime.GC()
		}
	}
	accounts = accounts[:accountIndex]
	fmt.Println("The invalid accounts number is ", invalidCounts)
	fmt.Println("The valid accounts number is ", len(accounts))
	return accounts, cexAssetsInfo, nil
}

func ConvertFloatStrToUint64(f string, multiplier int64) (uint64, error) {
	if f == "0.0" {
		return 0, nil
	}
	numFloat, err := decimal.NewFromString(f)
	if err != nil {
		return 0, err
	}
	numFloat = numFloat.Mul(decimal.NewFromInt(multiplier))
	numBigInt := numFloat.BigInt()
	if !numBigInt.IsUint64() {
		return 0, errors.New("overflow uint64")
	}
	num := numBigInt.Uint64()
	return num, nil
}

func DecodeBatchWitness(data string) *BatchCreateUserWitness {
	var witnessForCircuit BatchCreateUserWitness
	b, err := base64.StdEncoding.DecodeString(data)
	if err != nil {
		fmt.Println("deserialize batch witness failed: ", err.Error())
		return nil
	}
	unserializeBuf := bytes.NewBuffer(b)
	dec := gob.NewDecoder(unserializeBuf)
	err = dec.Decode(&witnessForCircuit)
	if err != nil {
		fmt.Println("unmarshal batch witness failed: ", err.Error())
		return nil
	}
	for i := 0; i < len(witnessForCircuit.CreateUserOps); i++ {
		userAssets := make([]AccountAsset, AssetCounts)
		storeUserAssets := witnessForCircuit.CreateUserOps[i].Assets
		for p := 0; p < len(storeUserAssets); p++ {
			userAssets[storeUserAssets[p].Index] = storeUserAssets[p]
		}
		witnessForCircuit.CreateUserOps[i].Assets = userAssets
	}
	return &witnessForCircuit
}

func AccountInfoToHash(account *AccountInfo, hasher *hash.Hash) []byte {
	assetCommitment := ComputeUserAssetsCommitment(hasher, account.Assets)
	(*hasher).Reset()
	// compute new account leaf node hash
	accountHash := poseidon.PoseidonBytes(account.AccountId, account.TotalEquity.Bytes(), account.TotalDebt.Bytes(), assetCommitment)
	return accountHash
}

func RecoverAfterCexAssets(witness *BatchCreateUserWitness) []CexAssetInfo {
	cexAssets := witness.BeforeCexAssets
	for i := 0; i < len(witness.CreateUserOps); i++ {
		for j := 0; j < len(witness.CreateUserOps[i].Assets); j++ {
			asset := &witness.CreateUserOps[i].Assets[j]
			cexAssets[asset.Index].TotalEquity = SafeAdd(cexAssets[asset.Index].TotalEquity, asset.Equity)
			cexAssets[asset.Index].TotalDebt = SafeAdd(cexAssets[asset.Index].TotalDebt, asset.Debt)
		}
	}
	// sanity check
	hasher := poseidon.NewPoseidon()
	for i := 0; i < len(cexAssets); i++ {
		commitment := ConvertAssetInfoToBytes(cexAssets[i])
		hasher.Write(commitment)
	}
	cexCommitment := hasher.Sum(nil)
	if string(cexCommitment) != string(witness.AfterCEXAssetsCommitment) {
		panic("after cex commitment verify failed")
	}
	return cexAssets
}

func ComputeCexAssetsCommitment(cexAssetsInfo []CexAssetInfo) []byte {
	hasher := poseidon.NewPoseidon()
	emptyCexAssets := make([]CexAssetInfo, AssetCounts-len(cexAssetsInfo))
	cexAssetsInfo = append(cexAssetsInfo, emptyCexAssets...)
	for i := 0; i < len(cexAssetsInfo); i++ {
		commitment := ConvertAssetInfoToBytes(cexAssetsInfo[i])
		hasher.Write(commitment)
	}
	return hasher.Sum(nil)
}
