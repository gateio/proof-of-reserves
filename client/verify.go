package client

import (
	"gate-zkmerkle-proof/service/verify_service"
	"github.com/spf13/cobra"
)

func VerifyCommand() *cobra.Command {
	cmd := &cobra.Command{
		Use:   "verify",
		Short: "verify proof",
	}

	cmd.AddCommand(
		VerifyCexCommand(),
		VerifyUserCommand(),
	)
	return cmd
}

func VerifyCexCommand() *cobra.Command {
	cmd := &cobra.Command{
		Use:   "cex",
		Short: "verify cex proof",
		Run: func(cmd *cobra.Command, args []string) {
			verify_service.CexVerify()
		},
	}
	return cmd
}

func VerifyUserCommand() *cobra.Command {
	cmd := &cobra.Command{
		Use:   "user",
		Short: "verify user proof",
		Run: func(cmd *cobra.Command, args []string) {
			verify_service.UserVerify()
		},
	}
	return cmd
}
