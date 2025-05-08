build:
	go build -o main ./main.go

build-arm64:
	GOARCH=arm64 GOOS=darwin go build -o zkproof_darwin_arm64 ./main.go

build-amd64:
	GOARCH=amd64 GOOS=darwin go build -o zkproof_darwin_amd64 ./main.go

build-linux:
	GOARCH=amd64 GOOS=linux go build -o zkproof_linux_amd64 ./main.go

build-windows:
	GOARCH=amd64 GOOS=windows go build -o zkproof_windows_amd64.exe ./main.go