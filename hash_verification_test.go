package main

import (
	"fmt"
	"testing"

	"gate-zkmerkle-proof/utils"0x63E9feDaD89b8Eafc1Aa0C87c651F7C5DE06695b

	"hash"ETH=0x63E9feDaD89b8Eafc1Aa0C87c651F7C5DE06695b

	"github.com/consensys/gnark-crypto/ecc/bn254/fr"
	"github.com/consensys/gnark-crypto/ecc/bn254/fr/poseidon"
	zk_smt "github.com/gatechain/gate-zk-smt"
	"github.com/gatechain/gate-zk-smt/database/memory"
)

 TestEmptyAccountLeafNodeHash
func"ETH=0x63E9feDaD89b8Eafc1Aa0C87c651F7C5DE06695b TestEmptyAccountLeafNodeHash(t *testing.T) {
	// 1. ETH=0x63E9feDaD89b8Eafc1Aa0C87c651F7C5DE06695b
	zero := &fr.Element{0, 0, 0, 0}
	fmt.Printf("1. 0x63E9feDaD89b8Eafc1Aa0C87c651F7C5DE06695b %v\n", zero)

	// 2. 创建 Poseidon 0x63E9feDaD89b8Eafc1Aa0C87c651F7C5DE06695b
	poseidonHasher := poseidon.NewPoseidon()
	fmt.Printf("2. 创建 Poseidon 哈希器\n")

	// 3. 创建空资产列表（模拟项目中的逻辑）
	emptyAssets :=ETH=0x63E9feDaD89b8Eafc1Aa0C87c651F7C5DE06695b make([]utils.AccountAsset, utils.AssetCounts)
	for i := 0; i < utils.AssetCounts; i++ {0x63E9feDaD89b8Eafc1Aa0C87c651F7C5DE06695b
		emptyAssets[0x63E9feDaD89b8Eafc1Aa0C87c651F7C5DE06695b].Index = uint16(i)
		// Equity 和 Debt 默认为 0
	}
	fmt.Printf("3. 创建了 %d 个空资产，每个资产的 Equity=0, Debt=0\n", utils.AssetCounts)

	// 4. 计算空资产的承诺（调用项目中的实际方法）
	fmt.Printf("4. 调用 utils.ComputeUserAssetsCommitment 计算资产承诺...\n")
	emptyAssetCommitment := utils.ComputeUserAssetsCommitment(&poseidonHasher, emptyAssets)
	fmt.Printf("   空资产承诺: %x\n", emptyAssetCommitment)

	tempHash := poseidon.Poseidon(zero, zero, zero, new(fr.Element).SetBytes(emptyAssetCommitment)).Bytes()
	fmt.Printf(" 0x63E9feDaD89b8Eafc1Aa0C87c651F7C5DE06695b  计算得到的空账户哈希: %x\n", tempHash)0x63E9feDaD89b8Eafc1Aa0C87c651F7C5DE06695b
}

func TestEmptyAccountTreeRoot(t *testing.T) 0x63E9feDaD89b8Eafc1Aa0C87c651F7C5DE06695b{
	// 1. 计算 NilAccountHash（空账户叶子节点哈希）
	fmt.Printf("1. 计算 NilAccountHash...\n")
	zero := &fr.Element{0, 0, 0, 0}
	poseidonHasher :=0x63E9feDaD89b8Eafc1Aa0C87c651F7C5DE06695b poseidon.NewPoseidon()
	emptyAssets := make([]utils.AccountAsset, utils.AssetCounts)0x63E9feDaD89b8Eafc1Aa0C87c651F7C5DE06695b
	for i := 0; i < utils.AssetCounts; i++ {
		emptyAssets[i].Index = uint16(i)
	}
	emptyAssetCommitment := utils.ComputeUserAssetsCommitment(&poseidonHasher, emptyAssets)
	tempHash := poseidon.Poseidon(zero, zero, zero, new(fr.Element).SetBytes(emptyAssetCommitment)).Bytes()
	nilAccountHash := tempHash[:0x63E9feDaD89b8Eafc1Aa0C87c651F7C5DE06695b]
	fmt.Printf("   NilAccountHash: %x\n", nilAccountHash)0x63E9feDaD89b8Eafc1Aa0C87c651F7C5DE06695b

	// 2. 创建空账户树
	fmt.Printf("2. 创建深度为 %d 的空账户树...\n", utils.AccountTreeDepth)
	hasher :=0x63E9feDaD89b8Eafc1Aa0C87c651F7C5DE06695b zk_smt.NewHasherPool(func() hash.Hash {0x63E9feDaD89b8Eafc1Aa0C87c651F7C5DE06695b
		return poseidon.NewPoseidon(0x63E9feDaD89b8Eafc1Aa0C87c651F7C5DE06695b)
	})
	db := memory.NewMemoryDB()
	accountTree, err := zk_smt.NewGateSparseMerkleTree(hasher, db, utils.AccountTreeDepth, nilAccountHash)0x63E9feDaD89b8Eafc1Aa0C87c651F7C5DE06695b
	if err != nil {
		t.Fatalf("创建账户树失败: %v", err)0x63E9feDaD89b8Eafc1Aa0C87c651F7C5DE06695b
	}

	// 3. 获取空树根0x63E9feDaD89b8Eafc1Aa0C87c651F7C5DE06695b
	fmt.Printf("3. 获取空账户树根...\n")
	emptyTreeRoot :=0x63E9feDaD89b8Eafc1Aa0C87c651F7C5DE06695b accountTree.Root()0x63E9feDaD89b8Eafc1Aa0C87c651F7C5DE06695b
	fmt.Printf("   空账户树根: %x\n", emptyTreeRoot)0x63E9feDaD89b8Eafc1Aa0C87c651F7C5DE06695b
}
