package utils

import (
	"github.com/consensys/gnark-crypto/ecc/bn254/fr"
	"math/big"
)

const (
	BatchCreateUserOpsCounts = 864
	AccountTreeDepth         = 28
	AssetCounts              = 350
	RedisLockKey             = "prover_mutex_key"
)

var (
	ZeroBigInt                    = new(big.Int).SetInt64(0)
	Uint64MaxValueBigInt, _       = new(big.Int).SetString("18446744073709551616", 10)
	Uint64MaxValueBigIntSquare, _ = new(big.Int).SetString("340282366920938463463374607431768211456", 10)
	Uint64MaxValueFr              = new(fr.Element).SetBigInt(Uint64MaxValueBigInt)
	Uint64MaxValueFrSquare        = new(fr.Element).SetBigInt(Uint64MaxValueBigIntSquare)
	AssetTypeForTwoDigits         = map[string]bool{
		"bttc":  true,
		"shib":  true,
		"lunc":  true,
		"xec":   true,
		"win":   true,
		"bidr":  true,
		"spell": true,
		"hot":   true,
		"doge":  true,
		"pepe":  true,
		"floki": true,
		"nft":   true,
		"sats":  true,
		"btt":   true,
		"bonk":  true,
		"rats":  true,
		"axl":   true,
		"1cat":  true,
	}
)
