package circuit

import (
	"gate-zkmerkle-proof/utils"
	"github.com/consensys/gnark/std/hash/poseidon"
)

func VerifyMerkleProof(api API, merkleRoot Variable, node Variable, proofSet, helper []Variable) {
	for i := 0; i < len(proofSet); i++ {
		api.AssertIsBoolean(helper[i])
		d1 := api.Select(helper[i], proofSet[i], node)
		d2 := api.Select(helper[i], node, proofSet[i])
		node = poseidon.Poseidon(api, d1, d2)
	}
	// Compare our calculated Merkle root to the desired Merkle root.
	api.AssertIsEqual(merkleRoot, node)
}

func UpdateMerkleProof(api API, node Variable, proofSet, helper []Variable) (root Variable) {
	for i := 0; i < len(proofSet); i++ {
		api.AssertIsBoolean(helper[i])
		d1 := api.Select(helper[i], proofSet[i], node)
		d2 := api.Select(helper[i], node, proofSet[i])
		node = poseidon.Poseidon(api, d1, d2)
	}
	root = node
	return root
}

func AccountIdToMerkleHelper(api API, accountId Variable) []Variable {
	merkleHelpers := api.ToBinary(accountId, utils.AccountTreeDepth)
	return merkleHelpers
}

// check value is in [0, 2^64-1] range
func CheckValueInRange(api API, value Variable) {
	api.ToBinary(value, 64)
}

func ComputeUserAssetsCommitment(api API, assets []UserAssetInfo) Variable {
	nEles := (len(assets)*2 + 2) / 3
	tmpUserAssets := make([]Variable, nEles)
	flattenAssets := make([]Variable, nEles*3)
	for i := 0; i < len(assets); i++ {
		flattenAssets[2*i] = assets[i].Equity
		flattenAssets[2*i+1] = assets[i].Debt
	}
	for i := len(assets) * 2; i < len(flattenAssets); i++ {
		flattenAssets[i] = 0
	}
	for i := 0; i < len(tmpUserAssets); i++ {
		tmpUserAssets[i] = api.Add(api.Mul(flattenAssets[3*i], utils.Uint64MaxValueFrSquare),
			api.Mul(flattenAssets[3*i+1], utils.Uint64MaxValueFr), flattenAssets[3*i+2])
	}
	commitment := poseidon.Poseidon(api, tmpUserAssets...)
	return commitment
}
