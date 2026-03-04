BINARY=auditor
CMD=./cmd/auditor

.PHONY: build test install clean

build:
	go build -o $(BINARY) $(CMD)

test:
	go test ./...

install:
	go install $(CMD)

clean:
	rm -f $(BINARY)
