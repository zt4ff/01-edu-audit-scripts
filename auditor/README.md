# auditor

A CLI tool to fetch audit test scripts from [01-edu-audit-scripts](https://github.com/zt4ff/01-edu-audit-scripts).

## Install

### Via PPA (Ubuntu/Debian)
```bash
sudo add-apt-repository ppa:zt4ff/auditor
sudo apt update
sudo apt install auditor
```

### From source
```bash
git clone https://github.com/zt4ff/auditor.git
cd auditor
make install
```

## Usage

```bash
auditor <file-name> --script=<language>
```

### Examples

```bash
# Fetch the Python version of go-reloaded
auditor go-reloaded --script=py

# Fetch the Go version
auditor go-reloaded --script=go

# Fetch the Bash version and save to a custom path
auditor go-reloaded --script=bash --output=./tests/go-reloaded.sh

# Use a fork or mirror
auditor go-reloaded --script=py --repo=https://raw.githubusercontent.com/your-fork/01-edu-audit-scripts/main

# List supported languages
auditor list
```

## Supported Languages

| Flag   | Extension |
|--------|-----------|
| `py`   | `.py`     |
| `go`   | `.go`     |
| `bash` | `.sh`     |

## URL Pattern

Scripts are fetched from:
```
https://raw.githubusercontent.com/zt4ff/01-edu-audit-scripts/main/scripts/<lang>/<file-name>.<ext>
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
