build:
	go build ./main.go

build-linux:
	CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build ./main.go

build-windows:
	CGO_ENABLED=0 GOOS=windows GOARCH=amd64 go build ./main.go