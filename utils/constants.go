package utils

import (
	"math/big"

	"github.com/consensys/gnark-crypto/ecc/bn254/fr"
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
		"nft":      true,
		"turbo":    true,
		"cheems":   true,
		"hippo":    true,
		"spell":    true,
		"sats":     true,
		"qubic":    true,
		"pepe":     true,
		"lunc":     true,
		"snek":     true,
		"shib":     true,
		"dog":      true,
		"mog":      true,
		"vinu":     true,
		"lai":      true,
		"btt":      true,
		"1cat":     true,
		"wen":      true,
		"aidoge":   true,
		"bidr":     true,
		"elon":     true,
		"wgrt":     true,
		"say":      true,
		"bonk":     true,
		"pepper":   true,
		"rats":     true,
		"supra":    true,
		"hot":      true,
		"omi":      true,
		"htx":      true,
		"reef":     true,
		"peipei":   true,
		"wojak":    true,
		"xec":      true,
		"toshi":    true,
		"win":      true,
		"babydoge": true,
		"why":      true,
		"bome":     true,
		"doge":     true,
		"zbcn":     true,
		"bttc":     true,
		"raca":     true,
		"apepe":    true,
		"ladys":    true,
		"vra":      true,
		"axl":      true,
		"floki":    true,
		"bgsc":     true,
		"atlas":    true,
	}
)
