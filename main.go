package main

import (
	"fmt"
	"gate-zkmerkle-proof/client"
	"github.com/spf13/cobra"
	"os"
)

func main() {
	rootCmd := &cobra.Command{
		Use:   "gproof",
		Short: "Command line interface for interacting with gate-zkmerkle-proof",
	}

	rootCmd.AddCommand(
		client.KeygenCommand(),
		client.WitnessCommand(),
		client.ProverCommand(),
		client.UserProofCommand(),
		client.VerifyCommand(),
		client.ToolCommand(),
	)

	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
