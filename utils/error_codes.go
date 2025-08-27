package utils

import "errors"

var (
	DbErrSqlOperation  = errors.New("unknown sql operation error")
	DbErrNotFound      = errors.New("sql: no rows in result set")
	GetRedisLockFailed = errors.New("get lock failed")
)
