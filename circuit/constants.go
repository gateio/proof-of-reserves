package circuit

import "math/big"

var (
	//  is poseidon hash(empty account info)
	EmptyAccountLeafNodeHash, _ = new(big.Int).SetString("2853aadbbd06deb5d6a1389d23a89ff47658aaf4a45b287ecfd62df192bd91a4", 16)
)
