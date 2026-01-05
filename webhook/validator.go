package webhook

import (
	"crypto/hmac"
	"crypto/sha256"
	"encoding/hex"
	"errors"
	"fmt"
	"strings"
)

var (
	// ErrMissingSignature is returned when the X-Hub-Signature-256 header is missing
	ErrMissingSignature = errors.New("x-hub-signature-256 header is missing")
	// ErrInvalidSignature is returned when the signature doesn't match
	ErrInvalidSignature = errors.New("request signatures didn't match")
)

// ValidateSignature validates that the payload was sent from GitHub by validating SHA256.
//
// This function verifies webhook deliveries by:
// 1. Computing an HMAC-SHA256 hash of the payload using the secret token
// 2. Comparing it with the signature sent in the X-Hub-Signature-256 header
// 3. Using constant-time comparison to prevent timing attacks
//
// Args:
//   - payloadBody: original request body to verify
//   - secretToken: GitHub webhook secret token
//   - signatureHeader: header received from GitHub (x-hub-signature-256)
//
// Returns:
//   - error: nil if signature is valid, otherwise ErrMissingSignature or ErrInvalidSignature
//
// Example:
//
//	err := ValidateSignature([]byte("Hello, World!"), "It's a Secret to Everybody", "sha256=757107...")
//	if err != nil {
//	    // Handle invalid signature
//	}
func ValidateSignature(payloadBody []byte, secretToken string, signatureHeader string) error {
	// Check if signature header is present
	if signatureHeader == "" {
		return ErrMissingSignature
	}

	// Compute HMAC-SHA256 signature
	mac := hmac.New(sha256.New, []byte(secretToken))
	mac.Write(payloadBody)
	expectedMAC := mac.Sum(nil)
	expectedSignature := "sha256=" + hex.EncodeToString(expectedMAC)

	// Use constant-time comparison to prevent timing attacks
	if !hmac.Equal([]byte(expectedSignature), []byte(signatureHeader)) {
		return ErrInvalidSignature
	}

	return nil
}

// ComputeSignature computes the HMAC-SHA256 signature for a payload.
// This is primarily used for testing and generating signatures.
//
// Args:
//   - payloadBody: the payload to sign
//   - secretToken: the secret token to use for signing
//
// Returns:
//   - signature: the computed signature in the format "sha256=<hex>"
//   - hexHash: the hex-encoded hash without the "sha256=" prefix
func ComputeSignature(payloadBody []byte, secretToken string) (signature string, hexHash string) {
	mac := hmac.New(sha256.New, []byte(secretToken))
	mac.Write(payloadBody)
	hash := mac.Sum(nil)
	hexHash = hex.EncodeToString(hash)
	signature = "sha256=" + hexHash
	return signature, hexHash
}

// ParseSignatureHeader extracts the algorithm and hash from a signature header.
// Expected format: "sha256=<hex_hash>"
//
// Args:
//   - signatureHeader: the signature header value
//
// Returns:
//   - algorithm: the hashing algorithm (e.g., "sha256")
//   - hash: the hex-encoded hash value
//   - error: nil if parsing succeeded, otherwise an error
func ParseSignatureHeader(signatureHeader string) (algorithm string, hash string, err error) {
	parts := strings.SplitN(signatureHeader, "=", 2)
	if len(parts) != 2 {
		return "", "", fmt.Errorf("invalid signature header format")
	}
	return parts[0], parts[1], nil
}
