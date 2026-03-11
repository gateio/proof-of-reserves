package verify_service

import (
	"bytes"
	"encoding/base64"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"gate-zkmerkle-proof/circuit"
	"gate-zkmerkle-proof/config"
	prover_server "gate-zkmerkle-proof/service/prover_service"
	"gate-zkmerkle-proof/utils"
	"github.com/consensys/gnark-crypto/ecc"
	"github.com/consensys/gnark-crypto/ecc/bn254/fr/poseidon"
	"github.com/consensys/gnark/backend/groth16"
	"github.com/consensys/gnark/frontend"
	"github.com/gocarina/gocsv"
	"io/ioutil"
	"os"
)

type Proof struct {
	BatchNumber        int64    `csv:"batch_number"`
	ZkProof            string   `csv:"proof_info"`
	CexAssetCommitment []string `csv:"cex_asset_list_commitments"`
	AccountTreeRoots   []string `csv:"account_tree_roots"`
	BatchCommitment    string   `csv:"batch_commitment"`
}

func CexVerify() {
	cexConfig := &config.CexConfig{}
	content, err := ioutil.ReadFile("./config/cex_config.json")
	if err != nil {
		panic(err.Error())
	}
	err = json.Unmarshal(content, cexConfig)
	if err != nil {
		panic(err.Error())
	}

	vk, err := prover_server.LoadVerifyingKey(cexConfig.ZkKeyVKDirectoryAndPrefix)
	if err != nil {
		panic(err.Error())
	}

	f, err := os.Open(cexConfig.ProofCsv)
	if err != nil {
		panic(err.Error())
	}
	defer f.Close()
	// index 4: proof_info, index 5: cex_asset_list_commitments
	// index 6: account_tree_roots, index 7: batch_commitment
	// index 8: batch_number

	tmpProofs := []*Proof{}

	err = gocsv.UnmarshalFile(f, &tmpProofs)
	if err != nil {
		panic(err.Error())
	}

	proofs := make([]Proof, len(tmpProofs))
	for i := 0; i < len(tmpProofs); i++ {
		proofs[tmpProofs[i].BatchNumber] = *tmpProofs[i]
	}

	batchNumber := int64(0)
	prevCexAssetListCommitments := make([][]byte, 2)
	prevAccountTreeRoots := make([][]byte, 2)
	// depth-28 empty account tree root
	emptyAccountTreeRoot, err := hex.DecodeString("0118925954da77d1a4b241fd163e4373e2265c515cfa60af7fcd28c8cb9ad58a")
	if err != nil {
		fmt.Println("wrong empty empty account tree root")
		return
	}
	prevAccountTreeRoots[1] = emptyAccountTreeRoot
	// according to asset price info to compute
	cexAssetsInfo := make([]utils.CexAssetInfo, len(cexConfig.CexAssetsInfo))
	for i := 0; i < len(cexConfig.CexAssetsInfo); i++ {
		cexAssetsInfo[cexConfig.CexAssetsInfo[i].Index] = cexConfig.CexAssetsInfo[i]
		if cexConfig.CexAssetsInfo[i].TotalEquity < cexConfig.CexAssetsInfo[i].TotalDebt {
			fmt.Printf("%s asset equity %d less then debt %d\n", cexConfig.CexAssetsInfo[i].Symbol, cexConfig.CexAssetsInfo[i].TotalEquity, cexConfig.CexAssetsInfo[i].TotalDebt)
			panic("invalid cex asset info")
		}
	}
	emptyCexAssetsInfo := make([]utils.CexAssetInfo, len(cexAssetsInfo))
	copy(emptyCexAssetsInfo, cexAssetsInfo)
	for i := 0; i < len(emptyCexAssetsInfo); i++ {
		emptyCexAssetsInfo[i].TotalDebt = 0
		emptyCexAssetsInfo[i].TotalEquity = 0
	}
	emptyCexAssetListCommitment := utils.ComputeCexAssetsCommitment(emptyCexAssetsInfo)
	expectFinalCexAssetsInfoComm := utils.ComputeCexAssetsCommitment(cexAssetsInfo)
	prevCexAssetListCommitments[1] = emptyCexAssetListCommitment
	var finalCexAssetsInfoComm []byte
	var accountTreeRoot []byte
	for i := 0; i < len(proofs); i++ {
		if batchNumber != proofs[i].BatchNumber {
			panic("the batch number is not monotonically increasing by 1")
		}
		// first deserialize proof
		proof := groth16.NewProof(ecc.BN254)
		var bufRaw bytes.Buffer
		proofRaw, err := base64.StdEncoding.DecodeString(proofs[i].ZkProof)
		if err != nil {
			fmt.Println("decode proof failed:", batchNumber)
			return
		}
		bufRaw.Write(proofRaw)
		proof.ReadFrom(&bufRaw)
		// deserialize cex asset list commitment and account tree root
		cexAssetListCommitments := make([][]byte, 2)
		accountTreeRoots := make([][]byte, 2)

		for j := 0; j < len(proofs[i].CexAssetCommitment); j++ {
			cexAssetListCommitments[j], err = base64.StdEncoding.DecodeString(proofs[i].CexAssetCommitment[j])
			if err != nil {
				fmt.Println("decode cex asset commitment failed")
				panic(err.Error())
			}
		}
		fmt.Println("=======================")
		fmt.Println(base64.StdEncoding.EncodeToString(cexAssetListCommitments[0]))
		fmt.Println(base64.StdEncoding.EncodeToString(cexAssetListCommitments[1]))
		fmt.Println("=======================")
		for j := 0; j < len(proofs[i].AccountTreeRoots); j++ {
			accountTreeRoots[j], err = base64.StdEncoding.DecodeString(proofs[i].AccountTreeRoots[j])
			if err != nil {
				fmt.Println("decode account tree root failed")
				panic(err.Error())
			}
		}

		finalCexAssetsInfoComm = cexAssetListCommitments[1]
		// verify the public input is correctly computed by cex asset list and account tree root
		poseidonHasher := poseidon.NewPoseidon()
		poseidonHasher.Write(accountTreeRoots[0])
		poseidonHasher.Write(accountTreeRoots[1])
		poseidonHasher.Write(cexAssetListCommitments[0])
		poseidonHasher.Write(cexAssetListCommitments[1])
		expectHash := poseidonHasher.Sum(nil)
		actualHash, err := base64.StdEncoding.DecodeString(proofs[i].BatchCommitment)
		if err != nil {
			fmt.Println("decode batch commitment failed", batchNumber)
			return
		}
		if string(expectHash) != string(actualHash) {
			fmt.Println("public input verify failed ", batchNumber)
			fmt.Printf("%x:%x\n", expectHash, actualHash)
			return
		}

		if string(accountTreeRoots[0]) != string(prevAccountTreeRoots[1]) ||
			string(cexAssetListCommitments[0]) != string(prevCexAssetListCommitments[1]) {
			fmt.Println(base64.StdEncoding.EncodeToString(cexAssetListCommitments[0]))
			fmt.Println(base64.StdEncoding.EncodeToString(prevCexAssetListCommitments[1]))
			fmt.Println("mismatch account tree root or cex asset list commitment:", batchNumber)
			return
		}
		prevCexAssetListCommitments = cexAssetListCommitments
		prevAccountTreeRoots = accountTreeRoots

		verifyWitness := circuit.NewVerifyBatchCreateUserCircuit(actualHash)
		vWitness, err := frontend.NewWitness(verifyWitness, ecc.BN254, frontend.PublicOnly())
		if err != nil {
			panic(err.Error())
		}
		err = groth16.Verify(proof, vk, vWitness)
		if err != nil {
			fmt.Println("proof verify failed:", batchNumber, err.Error())
			return
		} else {
			fmt.Println("proof verify success", batchNumber)
		}
		batchNumber++
		accountTreeRoot = accountTreeRoots[1]
	}
	if string(finalCexAssetsInfoComm) != string(expectFinalCexAssetsInfoComm) {
		panic("Final Cex Assets Info Not Match")
	}
	fmt.Printf("account merkle tree root is %x\n", accountTreeRoot)
	fmt.Println("All proofs verify passed!!!")
}

func UserVerify() {
	userConfig := &config.UserConfig{}
	content, err := ioutil.ReadFile("./config/user_config.json")
	if err != nil {
		panic(err.Error())
	}
	err = json.Unmarshal(content, userConfig)
	if err != nil {
		panic(err.Error())
	}
	root, err := hex.DecodeString(userConfig.TreeRootHash)
	if err != nil || len(root) != 32 {
		panic("invalid account tree root")
	}

	var proof [][]byte
	for i := 0; i < len(userConfig.MerkleProofEncode); i++ {
		p, err := base64.StdEncoding.DecodeString(userConfig.MerkleProofEncode[i])
		if err != nil || len(p) != 32 {
			panic("invalid proof")
		}
		proof = append(proof, p)
	}

	// padding user assets
	userAssets := make([]utils.AccountAsset, utils.AssetCounts)
	for i := 0; i < utils.AssetCounts; i++ {
		userAssets[i].Index = uint16(i)
	}
	for i := 0; i < len(userConfig.AssetDetails); i++ {
		userAssets[userConfig.AssetDetails[i].Index] = userConfig.AssetDetails[i]
	}
	hasher := poseidon.NewPoseidon()
	assetCommitment := utils.ComputeUserAssetsCommitment(&hasher, userAssets)
	hasher.Reset()
	// compute new account leaf node hash
	accountIdHash, err := hex.DecodeString(userConfig.UniqueIdentification)
	if err != nil || len(accountIdHash) != 32 {
		panic("the AccountIdHash is invalid")
	}
	accountHash := poseidon.PoseidonBytes(accountIdHash, userConfig.TotalAssetEquity.Bytes(), userConfig.TotalAssetDebt.Bytes(), assetCommitment)
	fmt.Printf("merkle leave hash: %x\n", accountHash)
	verifyFlag := utils.VerifyMerkleProof(root, userConfig.Arrangement, proof, accountHash)
	if verifyFlag {
		fmt.Println("verify pass!!!")
	} else {
		fmt.Println("verify failed...")
	}
}
