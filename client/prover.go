package client

import (
	prover_server "gate-zkmerkle-proof/service/prover_service"
	"github.com/spf13/cobra"
)

func ProverCommand() *cobra.Command {
	var pendingFlag bool
	cmd := &cobra.Command{
		Use:   "prover",
		Short: "used to generate zk proof and supports running in parallel",
		Run: func(cmd *cobra.Command, args []string) {
			prover_server.Handler(pendingFlag)
		},
	}
	cmd.Flags().BoolVarP(&pendingFlag, "pending", "p", false, "Specify pending status")
	return cmd
}
