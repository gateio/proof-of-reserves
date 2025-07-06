package utils

import (
	"context"
	"encoding/json"
	"errors"
	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/secretsmanager"
	"strings"
)

func GetSecretFromAws(secretId string) (string, error) {
	region := "ap-northeast-1"
	config, err := config.LoadDefaultConfig(context.TODO(), config.WithRegion(region))

	if err != nil {
		panic("Couldn't load config!")
	}
	conn := secretsmanager.NewFromConfig(config)

	result, err := conn.GetSecretValue(context.TODO(), &secretsmanager.GetSecretValueInput{
		SecretId: aws.String(secretId),
	})

	if err != nil {
		return "", err
	}

	return *result.SecretString, err
}

// user name can't include ":"
func GetMysqlSource(source string, secretId string) (string, error) {
	value, err := GetSecretFromAws(secretId)
	if err != nil {
		return "", err
	}

	var result map[string]string
	err = json.Unmarshal([]byte(value), &result)
	if err != nil {
		panic(err.Error())
	}
	passwd := result["pg_password"]
	aIndex := strings.Index(source, ":")
	bIndex := strings.Index(source, "@tcp")
	if aIndex == -1 || bIndex == -1 || bIndex <= aIndex {
		return "", errors.New("the source format is wrong")
	}
	newSource := source[:aIndex+1] + passwd + source[bIndex:]
	return newSource, nil
}
