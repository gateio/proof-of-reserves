package client

import (
	"gate-zkmerkle-proof/service/witness_service"
	"github.com/spf13/cobra"
)

func WitnessCommand() *cobra.Command {
	cmd := &cobra.Command{
		Use:   "witness",
		Short: "used to generate witness for prover service",
		Run: func(cmd *cobra.Command, args []string) {
			witness_service.Handler()
		},
	}
	return cmd
}
