package prover_server

import (
	"gate-zkmerkle-proof/utils"
	"gorm.io/gorm"
)

const (
	TableNamePrefix = "proof"
)

type (
	ProofModel interface {
		CreateProofTable() error
		DropProofTable() error
		CreateProof(row *Proof) error
		GetProofsBetween(start int64, end int64) (proofs []*Proof, err error)
		GetLatestProof() (p *Proof, err error)
		GetLatestConfirmedProof() (p *Proof, err error)
		GetProofByBatchNumber(height int64) (p *Proof, err error)
		GetProofNumber() (count int64)
		GetRowCounts() (count int64, err error)
	}

	defaultProofModel struct {
		table string
		DB    *gorm.DB
	}

	Proof struct {
		gorm.Model
		ProofInfo               string
		CexAssetListCommitments string
		AccountTreeRoots        string
		BatchCommitment         string
		BatchNumber             int64 `gorm:"index:idx_number,unique"`
	}
)

func (m *defaultProofModel) TableName() string {
	return m.table
}

func NewProofModel(db *gorm.DB, suffix string) ProofModel {
	return &defaultProofModel{
		table: TableNamePrefix + suffix,
		DB:    db,
	}
}

func (m *defaultProofModel) CreateProofTable() error {
	return m.DB.Table(m.table).AutoMigrate(Proof{})
}

func (m *defaultProofModel) DropProofTable() error {
	return m.DB.Migrator().DropTable(m.table)
}

func (m *defaultProofModel) CreateProof(row *Proof) error {
	dbTx := m.DB.Table(m.table).Create(row)
	if dbTx.Error != nil {
		return dbTx.Error
	}
	if dbTx.RowsAffected == 0 {
		return utils.DbErrSqlOperation
	}
	return nil
}

func (m *defaultProofModel) GetProofsBetween(start int64, end int64) (proofs []*Proof, err error) {
	dbTx := m.DB.Debug().Table(m.table).Where("batch_number >= ? AND batch_number <= ?",
		start,
		end).
		Order("batch_number").
		Find(&proofs)

	if dbTx.Error != nil {
		return proofs, utils.DbErrSqlOperation
	} else if dbTx.RowsAffected == 0 {
		return nil, utils.DbErrNotFound
	}

	return proofs, err
}

func (m *defaultProofModel) GetLatestProof() (p *Proof, err error) {
	var row *Proof
	dbTx := m.DB.Table(m.table).Order("batch_number desc").Limit(1).Find(&row)
	if dbTx.Error != nil {
		return nil, utils.DbErrSqlOperation
	} else if dbTx.RowsAffected == 0 {
		return nil, utils.DbErrNotFound
	} else {
		return row, nil
	}
}

func (m *defaultProofModel) GetLatestConfirmedProof() (p *Proof, err error) {
	var row *Proof
	dbTx := m.DB.Table(m.table).Order("batch_number desc").Limit(1).Find(&row)
	if dbTx.Error != nil {
		return nil, utils.DbErrSqlOperation
	} else if dbTx.RowsAffected == 0 {
		return nil, utils.DbErrNotFound
	} else {
		return row, nil
	}
}

func (m *defaultProofModel) GetProofByBatchNumber(num int64) (p *Proof, err error) {
	var row *Proof
	dbTx := m.DB.Table(m.table).Where("batch_number = ?", num).Find(&row)
	if dbTx.Error != nil {
		return nil, utils.DbErrSqlOperation
	} else if dbTx.RowsAffected == 0 {
		return nil, utils.DbErrNotFound
	} else {
		return row, nil
	}
}

func (m *defaultProofModel) GetProofNumber() (count int64) {
	m.DB.Raw("select count(*) from " + m.table).Count(&count)
	return count
}

func (m *defaultProofModel) GetRowCounts() (count int64, err error) {
	dbTx := m.DB.Table(m.table).Count(&count)
	if dbTx.Error != nil {
		return 0, dbTx.Error
	}
	return count, nil
}
