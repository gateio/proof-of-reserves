package userproof_service

import (
	"encoding/hex"
	"encoding/json"
	"fmt"
	"gate-zkmerkle-proof/config"
	"gate-zkmerkle-proof/global"
	"gate-zkmerkle-proof/utils"
	"github.com/consensys/gnark-crypto/ecc/bn254/fr/poseidon"
	zk_smt "github.com/gatechain/gate-zk-smt"
	"gorm.io/driver/mysql"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
	"io/ioutil"
	"log"
	"os"
	"time"
)

func HandleUserData(userProofConfig *config.Config) []utils.AccountInfo {
	startTime := time.Now().UnixMilli()
	accounts, _, err := utils.ReadUserAssets(userProofConfig.UserDataFile)
	if err != nil {
		panic(err.Error())
	}

	endTime := time.Now().UnixMilli()
	fmt.Println("handle user data cost ", endTime-startTime, " ms")
	return accounts
}

type AccountLeave struct {
	hash  []byte
	index uint32
}

func ComputeAccountRootHash(userProofConfig *config.Config) {
	accountTree, err := utils.NewAccountTree("memory", "")
	if err != nil {
		panic(err.Error())
	}
	accounts, _, err := utils.ReadUserAssets(userProofConfig.UserDataFile)
	if err != nil {
		panic(err.Error())
	}
	startTime := time.Now().UnixMilli()
	totalOpsNumber := len(accounts)
	fmt.Println("total ops number is ", totalOpsNumber)
	chs := make(chan AccountLeave, 1000)
	workers := 32
	results := make(chan bool, workers)
	averageAccounts := (totalOpsNumber + workers - 1) / workers
	actualWorkers := 0
	for i := 0; i < workers; i++ {
		srcAccountIndex := i * averageAccounts
		destAccountIndex := (i + 1) * averageAccounts
		if destAccountIndex > totalOpsNumber {
			destAccountIndex = totalOpsNumber
		}
		go CalculateAccountHash(accounts[srcAccountIndex:destAccountIndex], chs, results)
		if destAccountIndex == totalOpsNumber {
			actualWorkers = i + 1
			break
		}
	}
	fmt.Println("actual workers is ", actualWorkers)
	quit := make(chan bool, 1)
	go CalculateAccountTreeRoot(chs, &accountTree, quit)

	for i := 0; i < actualWorkers; i++ {
		<-results
	}
	close(chs)
	<-quit
	endTime := time.Now().UnixMilli()
	fmt.Println("user account tree generation cost ", endTime-startTime, " ms")
	fmt.Printf("account tree root %x\n", accountTree.Root())
}

func CalculateAccountHash(accounts []utils.AccountInfo, chs chan<- AccountLeave, res chan<- bool) {
	poseidonHasher := poseidon.NewPoseidon()
	for i := 0; i < len(accounts); i++ {
		chs <- AccountLeave{
			hash:  utils.AccountInfoToHash(&accounts[i], &poseidonHasher),
			index: accounts[i].AccountIndex,
		}
	}
	res <- true
}

func CalculateAccountTreeRoot(accountLeaves <-chan AccountLeave, accountTree *zk_smt.SparseMerkleTree, quit chan<- bool) {
	num := 0
	for accountLeaf := range accountLeaves {
		(*accountTree).Set(uint64(accountLeaf.index), accountLeaf.hash)
		num++
		if num%100000 == 0 {
			fmt.Println("for now, already set ", num, " accounts in tree")
		}
	}
	quit <- true
}

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

	userProofConfig := global.Cfg
	accountTree, err := utils.NewAccountTree(userProofConfig.TreeDB.Driver, userProofConfig.TreeDB.Option.Addr)
	accounts := HandleUserData(userProofConfig)
	fmt.Println("num", len(accounts))
	userProofModel := OpenUserProofTable(userProofConfig)
	latestAccountIndex, err := userProofModel.GetLatestAccountIndex()
	if err != nil && err != utils.DbErrNotFound {
		panic(err.Error())
	}
	if err == nil {
		latestAccountIndex += 1
	}
	accountTreeRoot := hex.EncodeToString(accountTree.Root())
	jobs := make(chan Job, 1000)
	nums := make(chan int, 1)
	results := make(chan *UserProof, 1000)
	for i := 0; i < 1; i++ {
		go worker(jobs, results, nums, accountTreeRoot)
	}
	quit := make(chan int, 1)
	for i := 0; i < 1; i++ {
		go WriteDB(results, userProofModel, quit, latestAccountIndex)
	}
	for i := int(latestAccountIndex); i < len(accounts); i++ {
		leaf, err := accountTree.Get(uint64(i), nil)
		if err != nil {
			panic(err.Error())
		}
		proof, err := accountTree.GetProof(uint64(accounts[i].AccountIndex))
		if err != nil {
			panic(err.Error())
		}
		jobs <- Job{
			account: &accounts[i],
			proof:   proof,
			leaf:    leaf,
		}
	}
	close(jobs)
	totalCounts := int(latestAccountIndex)
	for i := 0; i < 1; i++ {
		num := <-nums
		totalCounts += num
		fmt.Println("totalCounts", totalCounts)
	}
	if totalCounts != len(accounts) {
		fmt.Println("totalCounts actual:expected", totalCounts, len(accounts))
		panic("mismatch num")
	}
	close(results)
	for i := 0; i < 1; i++ {
		<-quit
	}
	fmt.Println("userproof service run finished...")
}

func WriteDB(results <-chan *UserProof, userProofModel UserProofModel, quit chan<- int, latestAccountIndex uint32) {
	index := 0
	proofs := make([]UserProof, 100)
	num := int(latestAccountIndex)
	for proof := range results {
		proofs[index] = *proof
		index += 1
		if index%100 == 0 {
			error := userProofModel.CreateUserProofs(proofs)
			if error != nil {
				panic(error.Error())
			}
			num += 100
			if num%100000 == 0 {
				fmt.Println("write ", num, "proof to db")
			}
			index = 0
		}
	}
	proofs = proofs[:index]
	if index > 0 {
		fmt.Println("write ", len(proofs), "proofs to db")
		userProofModel.CreateUserProofs(proofs)
		num += index
	}
	fmt.Println("total write ", num)
	quit <- 0
}

type Job struct {
	account *utils.AccountInfo
	proof   [][]byte
	leaf    []byte
}

func worker(jobs <-chan Job, results chan<- *UserProof, nums chan<- int, root string) {
	num := 0
	for job := range jobs {
		userProof := ConvertAccount(job.account, job.leaf, job.proof, root)
		results <- userProof
		num += 1
	}
	nums <- num
}

func ConvertAccount(account *utils.AccountInfo, leafHash []byte, proof [][]byte, root string) *UserProof {
	var userProof UserProof
	var userConfig UserConfig
	userProof.AccountIndex = account.AccountIndex
	userProof.AccountId = hex.EncodeToString(account.AccountId)
	userProof.AccountLeafHash = hex.EncodeToString(leafHash)
	proofSerial, err := json.Marshal(proof)
	userProof.Proof = string(proofSerial)
	assets, err := json.Marshal(account.Assets)
	if err != nil {
		panic(err.Error())
	}
	userProof.Assets = string(assets)
	userProof.TotalDebt = account.TotalDebt.String()
	userProof.TotalEquity = account.TotalEquity.String()

	userConfig.Arrangement = account.AccountIndex
	userConfig.UniqueIdentification = hex.EncodeToString(account.AccountId)
	userConfig.MerkleProofEncode = proof
	userConfig.TreeRootHash = root
	userConfig.AssetDetails = account.Assets
	userConfig.TotalAssetDebt = account.TotalDebt
	userConfig.TotalAssetEquity = account.TotalEquity
	configSerial, err := json.Marshal(userConfig)
	if err != nil {
		panic(err.Error())
	}
	userProof.Config = string(configSerial)
	return &userProof
}

func OpenUserProofTable(userConfig *config.Config) UserProofModel {
	newLogger := logger.New(
		log.New(os.Stdout, "\r\n", log.LstdFlags), // io writer
		logger.Config{
			SlowThreshold:             60 * time.Second, // Slow SQL threshold
			LogLevel:                  logger.Silent,    // Log level
			IgnoreRecordNotFoundError: true,             // Ignore ErrRecordNotFound error for logger
			Colorful:                  false,            // Disable color
		},
	)
	db, err := gorm.Open(mysql.Open(userConfig.MysqlDataSource), &gorm.Config{
		Logger: newLogger,
	})
	if err != nil {
		panic(err.Error())
	}
	userProofTable := NewUserProofModel(db, userConfig.DbSuffix)
	userProofTable.CreateUserProofTable()
	return userProofTable
}
