package prover_server

import (
	"encoding/json"
	"fmt"
	"gate-zkmerkle-proof/config"
	"gate-zkmerkle-proof/global"
	"os"
)

func Handler(pendingFlag bool) {
	global.Cfg = &config.Config{}
	jsonFile, err := os.ReadFile("./config/config.json")
	if err != nil {
		panic(fmt.Sprintf("load config err : %s", err.Error()))
	}
	err = json.Unmarshal(jsonFile, global.Cfg)
	if err != nil {
		panic(err.Error())
	}

	prover := NewProver(global.Cfg)
	prover.Run(pendingFlag)
}
