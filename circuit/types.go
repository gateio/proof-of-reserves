package circuit

import (
	"gate-zkmerkle-proof/utils"
	"github.com/consensys/gnark/frontend"
)

type (
	Variable = frontend.Variable
	API      = frontend.API
)

type CexAssetInfo struct {
	TotalEquity Variable
	TotalDebt   Variable
	BasePrice   Variable
}

type UserAssetInfo struct {
	Equity Variable
	Debt   Variable
}

type CreateUserOperation struct {
	BeforeAccountTreeRoot Variable
	AfterAccountTreeRoot  Variable
	Assets                []UserAssetInfo
	AccountIndex          Variable
	AccountIdHash         Variable
	AccountProof          [utils.AccountTreeDepth]Variable
}
