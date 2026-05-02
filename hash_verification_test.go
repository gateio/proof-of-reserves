package main

import (
	"fmt"
	"testing"

	"gate-zkmerkle-proof/utils"

	"hash"

	"github.com/consensys/gnark-crypto/ecc/bn254/fr"
	"github.com/consensys/gnark-crypto/ecc/bn254/fr/poseidon"
	zk_smt "github.com/gatechain/gate-zk-smt"
	"github.com/gatechain/gate-zk-smt/database/memory"
)

// 电路常量 计算空账户叶子节点哈希 TestEmptyAccountLeafNodeHash
func TestEmptyAccountLeafNodeHash(t *testing.T) {
	// 1. 创建零值元素
	zero := &fr.Element{0, 0, 0, 0}
	fmt.Printf("1. 零值元素: %v\n", zero)

	// 2. 创建 Poseidon 哈希器
	poseidonHasher := poseidon.NewPoseidon()
	fmt.Printf("2. 创建 Poseidon 哈希器\n")

	// 3. 创建空资产列表（模拟项目中的逻辑）
	emptyAssets := make([]utils.AccountAsset, utils.AssetCounts)
	for i := 0; i < utils.AssetCounts; i++ {
		emptyAssets[i].Index = uint16(i)
		// Equity 和 Debt 默认为 0
	}
	fmt.Printf("3. 创建了 %d 个空资产，每个资产的 Equity=0, Debt=0\n", utils.AssetCounts)

	// 4. 计算空资产的承诺（调用项目中的实际方法）
	fmt.Printf("4. 调用 utils.ComputeUserAssetsCommitment 计算资产承诺...\n")
	emptyAssetCommitment := utils.ComputeUserAssetsCommitment(&poseidonHasher, emptyAssets)
	fmt.Printf("   空资产承诺: %x\n", emptyAssetCommitment)

	tempHash := poseidon.Poseidon(zero, zero, zero, new(fr.Element).SetBytes(emptyAssetCommitment)).Bytes()
	fmt.Printf("   计算得到的空账户哈希: %x\n", tempHash)
}

func TestEmptyAccountTreeRoot(t *testing.T) {
	// 1. 计算 NilAccountHash（空账户叶子节点哈希）
	fmt.Printf("1. 计算 NilAccountHash...\n")
	zero := &fr.Element{0, 0, 0, 0}
	poseidonHasher := poseidon.NewPoseidon()
	emptyAssets := make([]utils.AccountAsset, utils.AssetCounts)
	for i := 0; i < utils.AssetCounts; i++ {
		emptyAssets[i].Index = uint16(i)
	}
	emptyAssetCommitment := utils.ComputeUserAssetsCommitment(&poseidonHasher, emptyAssets)
	tempHash := poseidon.Poseidon(zero, zero, zero, new(fr.Element).SetBytes(emptyAssetCommitment)).Bytes()
	nilAccountHash := tempHash[:]
	fmt.Printf("   NilAccountHash: %x\n", nilAccountHash)

	// 2. 创建空账户树
	fmt.Printf("2. 创建深度为 %d 的空账户树...\n", utils.AccountTreeDepth)
	hasher := zk_smt.NewHasherPool(func() hash.Hash {
		return poseidon.NewPoseidon()
	})
	db := memory.NewMemoryDB()
	accountTree, err := zk_smt.NewGateSparseMerkleTree(hasher, db, utils.AccountTreeDepth, nilAccountHash)
	if err != nil {
		t.Fatalf("创建账户树失败: %v", err)
	}

	// 3. 获取空树根
	fmt.Printf("3. 获取空账户树根...\n")
	emptyTreeRoot := accountTree.Root()
	fmt.Printf("   空账户树根: %x\n", emptyTreeRoot)
}
