package circuit

import "math/big"

var (
	//  is poseidon hash(empty account info)
	EmptyAccountLeafNodeHash, _ = new(big.Int).SetString("221970e0ba2d0b02a979e616cf186305372e73aab1e74f749772c9fef54dbf91", 16)
)
