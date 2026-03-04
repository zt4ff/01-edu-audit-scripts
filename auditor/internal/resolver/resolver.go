package resolver

import (
	"fmt"
	"strings"
)

const defaultRepo = "https://raw.githubusercontent.com/zt4ff/01-edu-audit-scripts/main"

// supported maps language flags to file extensions
var supported = map[string]string{
	"py":   "py",
	"go":   "go",
	"bash": "sh",
}

// BuildURL constructs the raw GitHub URL for the given script and language.
// Example: go-reloaded + py -> .../scripts/py/go-reloaded.py
func BuildURL(fileName, lang, repo string) (string, error) {
	ext, ok := supported[strings.ToLower(lang)]
	if !ok {
		return "", fmt.Errorf("unsupported language %q — supported: py, go, bash", lang)
	}

	if repo == "" {
		repo = defaultRepo
	}

	repo = strings.TrimRight(repo, "/")
	url := fmt.Sprintf("%s/scripts/%s/%s.%s", repo, lang, fileName, ext)
	return url, nil
}

// SupportedLanguages returns the list of supported language flags.
func SupportedLanguages() []string {
	langs := make([]string, 0, len(supported))
	for k := range supported {
		langs = append(langs, k)
	}
	return langs
}
