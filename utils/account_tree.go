package utils

import (
	"github.com/consensys/gnark-crypto/ecc/bn254/fr"
	"github.com/consensys/gnark-crypto/ecc/bn254/fr/poseidon"
	zk_smt "github.com/gatechain/gate-zk-smt"
	"github.com/gatechain/gate-zk-smt/database"
	"github.com/gatechain/gate-zk-smt/database/memory"
	"github.com/gatechain/gate-zk-smt/database/redis"
	"hash"
	"time"
)

var (
	NilAccountHash []byte
)

func init() {
	zero := &fr.Element{0, 0, 0, 0}
	poseidonHasher := poseidon.NewPoseidon()
	emptyAssets := make([]AccountAsset, AssetCounts)
	for i := 0; i < AssetCounts; i++ {
		emptyAssets[i].Index = uint16(i)
	}
	emptyAssetCommitment := ComputeUserAssetsCommitment(&poseidonHasher, emptyAssets)
	tempHash := poseidon.Poseidon(zero, zero, zero, new(fr.Element).SetBytes(emptyAssetCommitment)).Bytes()
	NilAccountHash = tempHash[:]
	// fmt.Printf("NilAccountHash is %x\n", NilAccountHash)
}

func NewAccountTree(driver string, addr string) (accountTree zk_smt.SparseMerkleTree, err error) {

	hasher := zk_smt.NewHasherPool(func() hash.Hash {
		return poseidon.NewPoseidon()
	})

	var db database.TreeDB
	if driver == "memory" {
		db = memory.NewMemoryDB()
	} else if driver == "redis" {
		redisOption := &redis.RedisConfig{}
		redisOption.Addr = addr
		redisOption.DialTimeout = 10 * time.Second
		redisOption.ReadTimeout = 10 * time.Second
		redisOption.WriteTimeout = 10 * time.Second
		redisOption.PoolTimeout = 15 * time.Second
		redisOption.IdleTimeout = 5 * time.Minute
		redisOption.PoolSize = 500
		redisOption.MaxRetries = 5
		redisOption.MinRetryBackoff = 8 * time.Millisecond
		redisOption.MaxRetryBackoff = 512 * time.Millisecond
		db, err = redis.New(redisOption)
		if err != nil {
			return nil, err
		}
	}

	accountTree, err = zk_smt.NewGateSparseMerkleTree(hasher, db, AccountTreeDepth, NilAccountHash)
	if err != nil {
		return nil, err
	}
	return accountTree, nil
}

func VerifyMerkleProof(root []byte, accountIndex uint32, proof [][]byte, node []byte) bool {
	if len(proof) != AccountTreeDepth {
		return false
	}
	hasher := poseidon.NewPoseidon()
	for i := 0; i < AccountTreeDepth; i++ {
		bit := accountIndex & (1 << i)
		if bit == 0 {
			hasher.Write(node)
			hasher.Write(proof[i])
		} else {
			hasher.Write(proof[i])
			hasher.Write(node)
		}
		node = hasher.Sum(nil)
		hasher.Reset()
	}
	if string(node) != string(root) {
		return false
	}
	return true
}
