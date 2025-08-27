package witness_service

import (
	"encoding/json"
	"fmt"
	"gate-zkmerkle-proof/config"
	"gate-zkmerkle-proof/global"
	"gate-zkmerkle-proof/utils"
	zk_smt "github.com/gatechain/gate-zk-smt"
	"io/ioutil"
)

func Handler() {
	global.Cfg = &config.Config{}
	jsonFile, err := ioutil.ReadFile("./config/config.json")
	if err != nil {
		panic(fmt.Sprintf("load config err : %s", err.Error()))
	}
	err = json.Unmarshal(jsonFile, global.Cfg)
	if err != nil {
		panic(err.Error())
	}
	
	accounts, cexAssetsInfo, accountTree := accountTree(global.Cfg)
	witnessService := NewWitness(accountTree, uint32(len(accounts)), accounts, cexAssetsInfo, global.Cfg)
	witnessService.Run()
	fmt.Println("witness service run finished...")
}

func accountTree(witnessConfig *config.Config) ([]utils.AccountInfo, []utils.CexAssetInfo, zk_smt.SparseMerkleTree) {
	accounts, cexAssetsInfo, err := utils.ReadUserAssets(witnessConfig.UserDataFile)
	fmt.Println("the user account total is", len(accounts))
	if err != nil {
		panic(err.Error())
	}
	accountTree, err := utils.NewAccountTree(witnessConfig.TreeDB.Driver, witnessConfig.TreeDB.Option.Addr)
	if err != nil {
		panic(err.Error())
	}
	fmt.Println("the account tree init height is ", accountTree.LatestVersion())
	fmt.Printf("account tree root is %x\n", accountTree.Root())

	return accounts, cexAssetsInfo, accountTree
}
