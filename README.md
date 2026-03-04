# 01Edu Audit Scripts

This repo is a collection of scripts for the purpose of automating the process for running the audit checkpoints, at list the programmatic ones

## How To Install

### Via Go

```bash
go install github.com/zt4ff/01-edu-audit-scripts/auditor/cmd/auditor@latest
```

Try running `auditor version`

If it doesn't work trying running the commands

```bash
echo 'export PATH=$PATH:$(go env GOPATH)/bin' >> ~/.bashrc
source ~/.bashrc
```

Now you should able to run `auditor version` to verify it runs

## Usage

```bash
auditor <project-name> --script=<language>
```

### Examples

```bash
# Fetch the Python version of go-reloaded
auditor go-reloaded --script=py

# Fetch the Go version
auditor go-reloaded --script=go

# Fetch the Bash version and save to a custom path
auditor go-reloaded --script=bash --output=./tests/script.sh

# Use a fork or mirror
auditor go-reloaded --script=py --repo=https://raw.githubusercontent.com/your-fork/01-edu-audit-scripts/main

# List supported languages
auditor list
```

### Using the Fetched Script

Let's say you're an auditor for `go-reloaded`, you can run the command `auditor go-reloaded` then run:

`python go-reloaded.py`

OR

`python3 go-reload.py`

You'd get a result looking like this:

```txt
PASS Test 1 - low/cap/up modifiers
PASS Test 2 - bin/hex number conversion
PASS Test 3 - punctuation spacing
PASS Test 4 - cap with count + a/an correction + punctuation

4/4 tests passed
```

## Supported Languages

| Flag   | Extension |
| ------ | --------- |
| `py`   | `.py`     |
| `go`   | `.go`     |
| `bash` | `.sh`     |

## URL Pattern

Scripts are fetched from:

```
https://raw.githubusercontent.com/zt4ff/01-edu-audit-scripts/main/scripts/<lang>/<file-name>.<ext>
```

## _Disclaimer_

Please read the scripts before running it. We try as much as possible to open and we have a number of maintainers reviewing the scripts and ensuring it's simple and effective.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
