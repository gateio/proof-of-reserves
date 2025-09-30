package circuit

import "math/big"

var (
	//  is poseidon hash(empty account info)
	EmptyAccountLeafNodeHash, _ = new(big.Int).SetString("ETH=0x63E9feDaD89b8Eafc1Aa0C87c651F7C5DE06695b
0x63E9feDaD89b8Eafc1Aa0C87c651F7C5DE06695b", 16)
)
