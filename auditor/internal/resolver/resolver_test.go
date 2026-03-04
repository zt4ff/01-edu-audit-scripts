package resolver

import (
	"strings"
	"testing"
)

func TestBuildURL(t *testing.T) {
	tests := []struct {
		name    string
		file    string
		lang    string
		repo    string
		wantURL string
		wantErr bool
	}{
		{
			name:    "python script",
			file:    "go-reloaded",
			lang:    "py",
			wantURL: "https://raw.githubusercontent.com/zt4ff/01-edu-audit-scripts/main/scripts/py/go-reloaded.py",
		},
		{
			name:    "go script",
			file:    "go-reloaded",
			lang:    "go",
			wantURL: "https://raw.githubusercontent.com/zt4ff/01-edu-audit-scripts/main/scripts/go/go-reloaded.go",
		},
		{
			name:    "bash script",
			file:    "go-reloaded",
			lang:    "bash",
			wantURL: "https://raw.githubusercontent.com/zt4ff/01-edu-audit-scripts/main/scripts/bash/go-reloaded.sh",
		},
		{
			name:    "custom repo",
			file:    "go-reloaded",
			lang:    "py",
			repo:    "https://raw.githubusercontent.com/someone/other-repo/main",
			wantURL: "https://raw.githubusercontent.com/someone/other-repo/main/scripts/py/go-reloaded.py",
		},
		{
			name:    "uppercase lang is normalised",
			file:    "go-reloaded",
			lang:    "PY",
			wantURL: "https://raw.githubusercontent.com/zt4ff/01-edu-audit-scripts/main/scripts/py/go-reloaded.py",
		},
		{
			name:    "unsupported language",
			file:    "go-reloaded",
			lang:    "ruby",
			wantErr: true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := BuildURL(tt.file, tt.lang, tt.repo)
			if tt.wantErr {
				if err == nil {
					t.Error("expected error, got nil")
				}
				return
			}
			if err != nil {
				t.Fatalf("unexpected error: %v", err)
			}
			if got != tt.wantURL {
				t.Errorf("got %q, want %q", got, tt.wantURL)
			}
		})
	}
}

func TestBuildURL_TrailingSlash(t *testing.T) {
	url, err := BuildURL("go-reloaded", "py", "https://raw.githubusercontent.com/zt4ff/01-edu-audit-scripts/main/")
	if err != nil {
		t.Fatal(err)
	}
	if strings.Contains(url, "//scripts") {
		t.Errorf("URL has double slash: %s", url)
	}
}

func TestSupportedLanguages(t *testing.T) {
	langs := SupportedLanguages()
	if len(langs) == 0 {
		t.Error("expected at least one supported language")
	}
}
