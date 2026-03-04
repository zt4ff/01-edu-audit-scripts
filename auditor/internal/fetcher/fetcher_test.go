package fetcher

import (
	"net/http"
	"net/http/httptest"
	"os"
	"path/filepath"
	"testing"
)

func TestDownload_Success(t *testing.T) {
	content := "print('hello world')"
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		w.Write([]byte(content))
	}))
	defer server.Close()

	tmp := t.TempDir()
	outPath := filepath.Join(tmp, "test.py")

	got, err := Download(server.URL+"/scripts/py/test.py", outPath)
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}

	data, _ := os.ReadFile(got)
	if string(data) != content {
		t.Errorf("got %q, want %q", string(data), content)
	}
}

func TestDownload_NotFound(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusNotFound)
	}))
	defer server.Close()

	_, err := Download(server.URL+"/scripts/py/missing.py", "")
	if err == nil {
		t.Error("expected error for 404, got nil")
	}
}

func TestDownload_NetworkError(t *testing.T) {
	_, err := Download("http://localhost:0/test.py", "")
	if err == nil {
		t.Error("expected network error, got nil")
	}
}

func TestDownload_DefaultOutputPath(t *testing.T) {
	server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		w.Write([]byte("content"))
	}))
	defer server.Close()

	tmp := t.TempDir()
	orig, _ := os.Getwd()
	os.Chdir(tmp)
	defer os.Chdir(orig)

	got, err := Download(server.URL+"/scripts/py/go-reloaded.py", "")
	if err != nil {
		t.Fatalf("unexpected error: %v", err)
	}
	if filepath.Base(got) != "go-reloaded.py" {
		t.Errorf("expected go-reloaded.py, got %s", filepath.Base(got))
	}
}
