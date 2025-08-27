package userproof_service

import (
	"gate-zkmerkle-proof/utils"
	"gorm.io/gorm"
	"math/big"
)

const TableNamePreifx = "userproof"

type (
	UserProofModel interface {
		CreateUserProofTable() error
		DropUserProofTable() error
		CreateUserProofs(rows []UserProof) error
		GetUserProofByIndex(id uint32) (*UserProof, error)
		GetUserProofById(id string) (*UserProof, error)
		GetLatestAccountIndex() (uint32, error)
	}

	defaultUserProofModel struct {
		table string
		DB    *gorm.DB
	}

	UserProof struct {
		AccountIndex    uint32 `gorm:"index:idx_int,unique"`
		AccountId       string `gorm:"index:idx_str,unique"`
		AccountLeafHash string
		TotalEquity     string
		TotalDebt       string
		Assets          string
		Proof           string
		Config          string
	}

	UserConfig struct {
		Arrangement          uint32
		UniqueIdentification string
		TotalAssetEquity     *big.Int
		TotalAssetDebt       *big.Int
		AssetDetails         []utils.AccountAsset
		TreeRootHash         string
		MerkleProofEncode    [][]byte
	}
)

func (m *defaultUserProofModel) TableName() string {
	return m.table
}

func NewUserProofModel(db *gorm.DB, suffix string) UserProofModel {
	return &defaultUserProofModel{
		table: TableNamePreifx + suffix,
		DB:    db,
	}
}

func (m *defaultUserProofModel) CreateUserProofTable() error {
	return m.DB.Table(m.table).AutoMigrate(UserProof{})
}

func (m *defaultUserProofModel) DropUserProofTable() error {
	return m.DB.Migrator().DropTable(m.table)
}

func (m *defaultUserProofModel) CreateUserProofs(rows []UserProof) error {
	dbTx := m.DB.Table(m.table).Create(rows)
	if dbTx.Error != nil {
		return dbTx.Error
	}
	return nil
}

func (m *defaultUserProofModel) GetUserProofByIndex(id uint32) (userproof *UserProof, err error) {
	dbTx := m.DB.Table(m.table).Where("account_index = ?", id).Find(userproof)
	if dbTx.Error != nil {
		return nil, dbTx.Error
	} else if dbTx.RowsAffected == 0 {
		return nil, utils.DbErrNotFound
	}
	return userproof, nil
}

func (m *defaultUserProofModel) GetUserProofById(id string) (userproof *UserProof, err error) {
	dbTx := m.DB.Table(m.table).Where("account_id = ?", id).Find(userproof)
	if dbTx.Error != nil {
		return nil, dbTx.Error
	} else if dbTx.RowsAffected == 0 {
		return nil, utils.DbErrNotFound
	}
	return userproof, nil
}

func (m *defaultUserProofModel) GetLatestAccountIndex() (uint32, error) {
	var row *UserProof
	dbTx := m.DB.Table(m.table).Order("account_index desc").Limit(1).Find(&row)
	if dbTx.Error != nil {
		return 0, dbTx.Error
	} else if dbTx.RowsAffected == 0 {
		return 0, utils.DbErrNotFound
	}
	return row.AccountIndex, nil
}
