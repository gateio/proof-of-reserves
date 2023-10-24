package client

import (
	"gate-zkmerkle-proof/service/tool_service"
	"github.com/spf13/cobra"
)

func ToolCommand() *cobra.Command {
	cmd := &cobra.Command{
		Use:   "tool",
		Short: "provide some common services",
	}

	cmd.AddCommand(
		ToolCleanKvrocks(),
		ToolCheckProverStatus(),
		ToolQueryCexAssets(),
	)
	return cmd
}

func ToolCleanKvrocks() *cobra.Command {
	cmd := &cobra.Command{
		Use:   "clean_kvrocks",
		Short: "remove only kvrocks data",
		Run: func(cmd *cobra.Command, args []string) {
			tool_service.CleanKvrocks()
		},
	}
	return cmd
}

func ToolCheckProverStatus() *cobra.Command {
	cmd := &cobra.Command{
		Use:   "check_prover_status",
		Short: "check prover data status",
		Run: func(cmd *cobra.Command, args []string) {
			tool_service.CheckProverStatus()
		},
	}
	return cmd
}

func ToolQueryCexAssets() *cobra.Command {
	cmd := &cobra.Command{
		Use:   "query_cex_assets",
		Short: "get cex assets info in json format",
		Run: func(cmd *cobra.Command, args []string) {
			tool_service.QueryCexAssets()
		},
	}
	return cmd
}
