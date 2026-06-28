package utils

import (
	"errors"
	"time"

	"github.com/zeromicro/go-zero/core/stores/redis"
)

const (
	LockExpiryTime = 10 // seconds
	RetryInterval  = 500 * time.Millisecond
	MaxRetryTimes  = 3
)

func GetRedisLockByKey(conn *redis.Redis, keyLock string) (redisLock *redis.RedisLock) {
	// get lock
	redisLock = redis.NewRedisLock(conn, keyLock)
	// set expiry time
	redisLock.SetExpire(LockExpiryTime)
	return redisLock
}

func TryAcquireLock(redisLock *redis.RedisLock) (err error) {
	// lock
	ok, err := redisLock.Acquire()
	if err != nil {
		return err
	}
	// re-try for three times
	if !ok {
		ticker := time.NewTicker(RetryInterval)
		defer ticker.Stop()
		count := 0
		for {
			if count > MaxRetryTimes {
				return errors.New("the lock has been used, re-try later")
			}
			ok, err = redisLock.Acquire()
			if err != nil {
				return err
			}
			if ok {
				break
			}
			count++
			<-ticker.C
		}
	}
	return nil
}
