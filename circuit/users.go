package circuit

import (
	"gate-zkmerkle-proof/utils"
	"github.com/consensys/gnark/std/hash/poseidon"
)

type BatchCreateUserCircuit struct {
	BatchCommitment           Variable `gnark:",public"`
	BeforeAccountTreeRoot     Variable
	AfterAccountTreeRoot      Variable
	BeforeCEXAssetsCommitment Variable
	AfterCEXAssetsCommitment  Variable
	BeforeCexAssets           []CexAssetInfo
	CreateUserOps             []CreateUserOperation
}

func NewVerifyBatchCreateUserCircuit(commitment []byte) *BatchCreateUserCircuit {
	var v BatchCreateUserCircuit
	v.BatchCommitment = commitment
	return &v
}

func NewBatchCreateUserCircuit(assetCounts uint32, batchCounts uint32) *BatchCreateUserCircuit {
	var circuit BatchCreateUserCircuit
	circuit.BatchCommitment = 0
	circuit.BeforeAccountTreeRoot = 0
	circuit.AfterAccountTreeRoot = 0
	circuit.BeforeCEXAssetsCommitment = 0
	circuit.AfterCEXAssetsCommitment = 0
	circuit.BeforeCexAssets = make([]CexAssetInfo, assetCounts)
	for i := uint32(0); i < assetCounts; i++ {
		circuit.BeforeCexAssets[i] = CexAssetInfo{
			TotalEquity: 0,
			TotalDebt:   0,
			BasePrice:   0,
		}
	}
	circuit.CreateUserOps = make([]CreateUserOperation, batchCounts)
	for i := uint32(0); i < batchCounts; i++ {
		circuit.CreateUserOps[i] = CreateUserOperation{
			BeforeAccountTreeRoot: 0,
			AfterAccountTreeRoot:  0,
			Assets:                make([]UserAssetInfo, assetCounts),
			AccountIndex:          0,
			AccountProof:          [utils.AccountTreeDepth]Variable{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
		}
		for j := uint32(0); j < assetCounts; j++ {
			circuit.CreateUserOps[i].Assets[j].Debt = 0
			circuit.CreateUserOps[i].Assets[j].Equity = 0
		}
	}
	return &circuit
}

func (b BatchCreateUserCircuit) Define(api API) error {
	// verify whether BatchCommitment is computed correctly
	actualBatchCommitment := poseidon.Poseidon(api, b.BeforeAccountTreeRoot, b.AfterAccountTreeRoot, b.BeforeCEXAssetsCommitment, b.AfterCEXAssetsCommitment)
	api.AssertIsEqual(b.BatchCommitment, actualBatchCommitment)
	cexAssets := make([]Variable, len(b.BeforeCexAssets))
	afterCexAssets := make([]CexAssetInfo, len(b.BeforeCexAssets))

	// verify whether beforeCexAssetsCommitment is computed correctly
	for i := 0; i < len(b.BeforeCexAssets); i++ {
		CheckValueInRange(api, b.BeforeCexAssets[i].TotalEquity)
		CheckValueInRange(api, b.BeforeCexAssets[i].TotalDebt)
		CheckValueInRange(api, b.BeforeCexAssets[i].BasePrice)
		cexAssets[i] = api.Add(api.Mul(b.BeforeCexAssets[i].TotalEquity, utils.Uint64MaxValueFrSquare),
			api.Mul(b.BeforeCexAssets[i].TotalDebt, utils.Uint64MaxValueFr), b.BeforeCexAssets[i].BasePrice)
		afterCexAssets[i] = b.BeforeCexAssets[i]
	}
	actualCexAssetsCommitment := poseidon.Poseidon(api, cexAssets...)
	api.AssertIsEqual(b.BeforeCEXAssetsCommitment, actualCexAssetsCommitment)

	api.AssertIsEqual(b.BeforeAccountTreeRoot, b.CreateUserOps[0].BeforeAccountTreeRoot)
	api.AssertIsEqual(b.AfterAccountTreeRoot, b.CreateUserOps[len(b.CreateUserOps)-1].AfterAccountTreeRoot)

	tempAfterCexAssets := make([]Variable, len(b.BeforeCexAssets))
	for i := 0; i < len(b.CreateUserOps); i++ {
		accountIndexHelper := AccountIdToMerkleHelper(api, b.CreateUserOps[i].AccountIndex)
		VerifyMerkleProof(api, b.CreateUserOps[i].BeforeAccountTreeRoot, EmptyAccountLeafNodeHash, b.CreateUserOps[i].AccountProof[:], accountIndexHelper)
		var totalUserEquity Variable = 0
		var totalUserDebt Variable = 0
		userAssets := b.CreateUserOps[i].Assets
		for j := 0; j < len(userAssets); j++ {
			CheckValueInRange(api, userAssets[j].Debt)
			CheckValueInRange(api, userAssets[j].Equity)
			totalUserEquity = api.Add(totalUserEquity, api.Mul(userAssets[j].Equity, b.BeforeCexAssets[j].BasePrice))
			totalUserDebt = api.Add(totalUserDebt, api.Mul(userAssets[j].Debt, b.BeforeCexAssets[j].BasePrice))

			afterCexAssets[j].TotalEquity = api.Add(afterCexAssets[j].TotalEquity, userAssets[j].Equity)
			afterCexAssets[j].TotalDebt = api.Add(afterCexAssets[j].TotalDebt, userAssets[j].Debt)
		}
		// make sure user's total Equity is greater than or equal to user's total Debt
		api.AssertIsLessOrEqual(totalUserDebt, totalUserEquity)

		userAssetsCommitment := ComputeUserAssetsCommitment(api, userAssets)
		accountHash := poseidon.Poseidon(api, b.CreateUserOps[i].AccountIdHash, totalUserEquity, totalUserDebt, userAssetsCommitment)
		actualAccountTreeRoot := UpdateMerkleProof(api, accountHash, b.CreateUserOps[i].AccountProof[:], accountIndexHelper)
		api.AssertIsEqual(actualAccountTreeRoot, b.CreateUserOps[i].AfterAccountTreeRoot)

	}

	for j := 0; j < len(tempAfterCexAssets); j++ {
		CheckValueInRange(api, afterCexAssets[j].TotalEquity)
		CheckValueInRange(api, afterCexAssets[j].TotalDebt)
		tempAfterCexAssets[j] = api.Add(api.Mul(afterCexAssets[j].TotalEquity, utils.Uint64MaxValueFrSquare),
			api.Mul(afterCexAssets[j].TotalDebt, utils.Uint64MaxValueFr), afterCexAssets[j].BasePrice)
	}

	// verify AfterCEXAssetsCommitment is computed correctly
	actualAfterCEXAssetsCommitment := poseidon.Poseidon(api, tempAfterCexAssets...)
	api.AssertIsEqual(actualAfterCEXAssetsCommitment, b.AfterCEXAssetsCommitment)

	for i := 0; i < len(b.CreateUserOps)-1; i++ {
		api.AssertIsEqual(b.CreateUserOps[i].AfterAccountTreeRoot, b.CreateUserOps[i+1].BeforeAccountTreeRoot)
	}

	return nil
}

func SetBatchCreateUserCircuitWitness(batchWitness *utils.BatchCreateUserWitness) (witness *BatchCreateUserCircuit, err error) {
	witness = &BatchCreateUserCircuit{
		BatchCommitment:           batchWitness.BatchCommitment,
		BeforeAccountTreeRoot:     batchWitness.BeforeAccountTreeRoot,
		AfterAccountTreeRoot:      batchWitness.AfterAccountTreeRoot,
		BeforeCEXAssetsCommitment: batchWitness.BeforeCEXAssetsCommitment,
		AfterCEXAssetsCommitment:  batchWitness.AfterCEXAssetsCommitment,
		BeforeCexAssets:           make([]CexAssetInfo, len(batchWitness.BeforeCexAssets)),
		CreateUserOps:             make([]CreateUserOperation, len(batchWitness.CreateUserOps)),
	}

	for i := 0; i < len(witness.BeforeCexAssets); i++ {
		witness.BeforeCexAssets[i].TotalEquity = batchWitness.BeforeCexAssets[i].TotalEquity
		witness.BeforeCexAssets[i].TotalDebt = batchWitness.BeforeCexAssets[i].TotalDebt
		witness.BeforeCexAssets[i].BasePrice = batchWitness.BeforeCexAssets[i].BasePrice
	}

	for i := 0; i < len(witness.CreateUserOps); i++ {
		witness.CreateUserOps[i].BeforeAccountTreeRoot = batchWitness.CreateUserOps[i].BeforeAccountTreeRoot
		witness.CreateUserOps[i].AfterAccountTreeRoot = batchWitness.CreateUserOps[i].AfterAccountTreeRoot
		witness.CreateUserOps[i].Assets = make([]UserAssetInfo, len(batchWitness.CreateUserOps[i].Assets))
		for j := 0; j < len(batchWitness.CreateUserOps[i].Assets); j++ {
			var userAsset UserAssetInfo
			userAsset.Equity = batchWitness.CreateUserOps[i].Assets[j].Equity
			userAsset.Debt = batchWitness.CreateUserOps[i].Assets[j].Debt
			witness.CreateUserOps[i].Assets[j] = userAsset
		}
		witness.CreateUserOps[i].AccountIdHash = batchWitness.CreateUserOps[i].AccountIdHash
		witness.CreateUserOps[i].AccountIndex = batchWitness.CreateUserOps[i].AccountIndex
		for j := 0; j < len(witness.CreateUserOps[i].AccountProof); j++ {
			witness.CreateUserOps[i].AccountProof[j] = batchWitness.CreateUserOps[i].AccountProof[j]
		}
	}
	return witness, nil
}
