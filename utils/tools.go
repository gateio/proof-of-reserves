package utils

import (
	"encoding/csv"
	"encoding/hex"
	"fmt"
	"github.com/consensys/gnark-crypto/ecc/bn254/fr"
	"golang.org/x/sync/syncmap"
	"io/ioutil"
	"math/big"
	"os"
	"path/filepath"
	"runtime"
	"strings"
	"time"
)

var UserIDS syncmap.Map

func ReadUserAssetsV1(dirname string) ([]AccountInfo, []CexAssetInfo, error) {
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
				tmpAccountInfo, tmpCexAssetInfo, err := ReadUserDataFromCsvFileV1(userFileNames[j])
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

func ReadUserDataFromCsvFileV1(name string) ([]AccountInfo, []CexAssetInfo, error) {
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

		cexAssetsInfo[i].BasePrice, err = ConvertFloatStrToUint64(data[0][assetCounts*3+i+2], multiplier)
		if err != nil {
			fmt.Println("asset data wrong:", data[0][assetCounts*3+i+2], err.Error())
			continue
		}
	}

	invalidCounts := 0
	for i := 0; i < len(data); i++ {
		// check userid is unique
		_, ok := UserIDS.Load(data[i][1])
		if ok {
			panic("accountId is Repeated : " + data[i][1])
		}
		UserIDS.Store(data[i][1], true)

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
				fmt.Println("account", data[i][1], "the symbol is ", cexAssetsInfo[j].Symbol, " ", data[i][j*3+2], " equity data wrong:", err.Error())
				invalidCounts += 1
				continue
			}

			debt, err := ConvertFloatStrToUint64(data[i][j*3+3], multiplier)
			if err != nil {
				fmt.Println("account", data[i][1], "the debt symbol is ", cexAssetsInfo[j].Symbol, " ", data[i][j*3+3], " debt data wrong:", err.Error())
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
