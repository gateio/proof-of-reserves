package tool_service

import (
	"context"
	"encoding/json"
	"fmt"
	"gate-zkmerkle-proof/config"
	"gate-zkmerkle-proof/global"
	prover_server "gate-zkmerkle-proof/service/prover_service"
	"gate-zkmerkle-proof/service/witness_service"
	"gate-zkmerkle-proof/utils"
	"github.com/go-redis/redis/v8"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
	"io/ioutil"
	"log"
	"os"
	"time"
)

func CleanKvrocks() {
	global.Cfg = &config.Config{}
	jsonFile, err := ioutil.ReadFile("./config/config.json")
	if err != nil {
		panic(fmt.Sprintf("load config err : %s", err.Error()))
	}
	err = json.Unmarshal(jsonFile, global.Cfg)
	if err != nil {
		panic(err.Error())
	}

	dbtoolConfig := global.Cfg
	client := redis.NewClient(&redis.Options{
		Addr:            dbtoolConfig.TreeDB.Option.Addr,
		PoolSize:        500,
		MaxRetries:      5,
		MinRetryBackoff: 8 * time.Millisecond,
		MaxRetryBackoff: 512 * time.Millisecond,
		DialTimeout:     10 * time.Second,
		ReadTimeout:     10 * time.Second,
		WriteTimeout:    10 * time.Second,
		PoolTimeout:     15 * time.Second,
		IdleTimeout:     5 * time.Minute,
	})
	client.FlushAll(context.Background())
	fmt.Println("kvrocks data drop successfully")
}

func CheckProverStatus() {
	global.Cfg = &config.Config{}
	jsonFile, err := ioutil.ReadFile("./config/config.json")
	if err != nil {
		panic(fmt.Sprintf("load config err : %s", err.Error()))
	}
	err = json.Unmarshal(jsonFile, global.Cfg)
	if err != nil {
		panic(err.Error())
	}

	dbtoolConfig := global.Cfg
	newLogger := logger.New(
		log.New(os.Stdout, "\r\n", log.LstdFlags), // io writer
		logger.Config{
			SlowThreshold:             60 * time.Second, // Slow SQL threshold
			LogLevel:                  logger.Silent,    // Log level
			IgnoreRecordNotFoundError: true,             // Ignore ErrRecordNotFound error for logger
			Colorful:                  false,            // Disable color
		},
	)
	db, err := gorm.Open(mysql.Open(dbtoolConfig.MysqlDataSource), &gorm.Config{
		Logger: newLogger,
	})
	if err != nil {
		panic(err.Error())
	}
	witnessModel := witness_service.NewWitnessModel(db, dbtoolConfig.DbSuffix)
	proofModel := prover_server.NewProofModel(db, dbtoolConfig.DbSuffix)

	witnessCounts, err := witnessModel.GetRowCounts()
	if err != nil {
		panic(err.Error())
	}
	proofCounts, err := proofModel.GetRowCounts()
	fmt.Printf("Total witness item %d, Published item %d, Pending item %d, Finished item %d\n", witnessCounts[0], witnessCounts[1], witnessCounts[2], witnessCounts[3])
	fmt.Println(witnessCounts[0] - proofCounts)
}

func QueryCexAssets() {
	global.Cfg = &config.Config{}
	jsonFile, err := ioutil.ReadFile("./config/config.json")
	if err != nil {
		panic(fmt.Sprintf("load config err : %s", err.Error()))
	}
	err = json.Unmarshal(jsonFile, global.Cfg)
	if err != nil {
		panic(err.Error())
	}

	dbtoolConfig := global.Cfg
	db, err := gorm.Open(mysql.Open(dbtoolConfig.MysqlDataSource))
	if err != nil {
		panic(err.Error())
	}
	witnessModel := witness_service.NewWitnessModel(db, dbtoolConfig.DbSuffix)
	latestWitness, err := witnessModel.GetLatestBatchWitness()
	if err != nil {
		panic(err.Error())
	}
	witness := utils.DecodeBatchWitness(latestWitness.WitnessData)
	if witness == nil {
		panic("decode invalid witness data")
	}
	cexAssetsInfo := utils.RecoverAfterCexAssets(witness)
	var newAssetsInfo []utils.CexAssetInfo
	for i := 0; i < len(cexAssetsInfo); i++ {
		if cexAssetsInfo[i].BasePrice != 0 {
			newAssetsInfo = append(newAssetsInfo, cexAssetsInfo[i])
		}
	}
	cexAssetsInfoBytes, _ := json.Marshal(newAssetsInfo)
	fmt.Println(string(cexAssetsInfoBytes))
}
