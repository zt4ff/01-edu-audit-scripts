package fetcher

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"time"
)

var httpClient = &http.Client{Timeout: 15 * time.Second}

// Download fetches the file at url and saves it to outputPath.
// If outputPath is empty, it saves to the current directory using the filename from the URL.
func Download(url, outputPath string) (string, error) {
	resp, err := httpClient.Get(url)
	if err != nil {
		return "", fmt.Errorf("network error: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode == http.StatusNotFound {
		return "", fmt.Errorf("script not found (404): %s", url)
	}
	if resp.StatusCode != http.StatusOK {
		return "", fmt.Errorf("unexpected status %d from %s", resp.StatusCode, url)
	}

	if outputPath == "" {
		outputPath = filepath.Base(url)
	}

	f, err := os.Create(outputPath)
	if err != nil {
		return "", fmt.Errorf("could not create file %q: %w", outputPath, err)
	}
	defer f.Close()

	if _, err := io.Copy(f, resp.Body); err != nil {
		return "", fmt.Errorf("error writing file: %w", err)
	}

	return outputPath, nil
}
