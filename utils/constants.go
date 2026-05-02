package utils

import (
	"math/big"

	"github.com/consensys/gnark-crypto/ecc/bn254/fr"
)

const (
	BatchCreateUserOpsCounts = 864
	AccountTreeDepth         = 28
	AssetCounts              = 800
	RedisLockKey             = "prover_mutex_key"
)

var (
	ZeroBigInt                    = new(big.Int).SetInt64(0)
	Uint64MaxValueBigInt, _       = new(big.Int).SetString("18446744073709551616", 10)
	Uint64MaxValueBigIntSquare, _ = new(big.Int).SetString("340282366920938463463374607431768211456", 10)
	Uint64MaxValueFr              = new(fr.Element).SetBigInt(Uint64MaxValueBigInt)
	Uint64MaxValueFrSquare        = new(fr.Element).SetBigInt(Uint64MaxValueBigIntSquare)
	AssetTypeForTwoDigits         = map[string]bool{
		"babydoge":   true,
		"omi":        true,
		"vra":        true,
		"qubic":      true,
		"btt":        true,
		"doge":       true,
		"peipei":     true,
		"raca":       true,
		"hot":        true,
		"vinu":       true,
		"wen":        true,
		"pig":        true,
		"shib":       true,
		"ladys":      true,
		"reef":       true,
		"why":        true,
		"bttc":       true,
		"bome":       true,
		"toshi":      true,
		"cheems":     true,
		"floki":      true,
		"bgsc":       true,
		"dsd":        true,
		"dbc":        true,
		"snek":       true,
		"sidus":      true,
		"dog":        true,
		"zbcn":       true,
		"sats":       true,
		"hippo":      true,
		"say":        true,
		"axl":        true,
		"coq":        true,
		"spell":      true,
		"htx":        true,
		"dogs":       true,
		"pepe":       true,
		"bidr":       true,
		"xec":        true,
		"elon":       true,
		"brise":      true,
		"apu":        true,
		"moodengeth": true,
		"wgrt":       true,
		"wojak":      true,
		"aidoge":     true,
		"kishu":      true,
		"wuf":        true,
		"bonk":       true,
		"maga":       true,
		"mog":        true,
		"xen":        true,
		"supra":      true,
		"x":          true,
		"pepper":     true,
		"lobo":       true,
		"turbo":      true,
		"nft":        true,
		"myria":      true,
		"apepe":      true,
		"troll":      true,
		"1cat":       true,
		"bitboard":   true,
		"lai":        true,
		"win":        true,
		"rats":       true,
		"lunc":       true,
		"natix":      true,
		"cat":        true,
		"atlas":      true,
		"zbai":       true,
		"akita":      true,
		"neirocto":   true,
		"lever":      true,
	}
)
