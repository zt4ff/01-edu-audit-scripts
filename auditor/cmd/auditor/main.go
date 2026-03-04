package main

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
	"github.com/zt4ff/01-edu-audit-scripts/auditor/internal/fetcher"
	"github.com/zt4ff/01-edu-audit-scripts/auditor/internal/resolver"
)

var (
	scriptLang string
	outputPath string
	repoURL    string
)

var rootCmd = &cobra.Command{
	Use:   "auditor <file-name>",
	Short: "Download audit test scripts from the 01-edu-audit-scripts repo",
	Long: `auditor fetches test scripts from https://github.com/zt4ff/01-edu-audit-scripts

Examples:
  auditor go-reloaded --script=py
  auditor go-reloaded --script=go
  auditor go-reloaded --script=bash --output=./tests/go-reloaded.sh`,
	Args: cobra.ExactArgs(1),
	RunE: func(cmd *cobra.Command, args []string) error {
		fileName := args[0]

		url, err := resolver.BuildURL(fileName, scriptLang, repoURL)
		if err != nil {
			return err
		}

		fmt.Printf("Fetching %s...\n", url)

		saved, err := fetcher.Download(url, outputPath)
		if err != nil {
			return err
		}

		fmt.Printf("Saved to %s\n", saved)
		return nil
	},
}

var listCmd = &cobra.Command{
	Use:   "list",
	Short: "List supported languages",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("Supported languages:")
		for _, lang := range resolver.SupportedLanguages() {
			fmt.Printf("  %s\n", lang)
		}
	},
}

var versionCmd = &cobra.Command{
	Use:   "version",
	Short: "Print the version",
	Run: func(cmd *cobra.Command, args []string) {
		fmt.Println("auditor v0.1.0")
	},
}

func init() {
	rootCmd.Flags().StringVarP(&scriptLang, "script", "s", "py", "language of the script: py, go, bash")
	rootCmd.Flags().StringVarP(&outputPath, "output", "o", "", "output file path (default: current directory)")
	rootCmd.Flags().StringVarP(&repoURL, "repo", "r", "", "custom repo base URL (overrides default)")

	rootCmd.AddCommand(listCmd)
	rootCmd.AddCommand(versionCmd)
}

func main() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
