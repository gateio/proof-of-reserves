package webhook

import (
	"testing"
)

// TestValidateSignature_ValidSignature tests successful signature validation
func TestValidateSignature_ValidSignature(t *testing.T) {
	// Using the test values from GitHub documentation
	secret := "It's a Secret to Everybody"
	payload := []byte("Hello, World!")
	expectedSignature := "sha256=757107ea0eb2509fc211221cce984b8a37570b6d7586c22c46f4379c8b043e17"

	err := ValidateSignature(payload, secret, expectedSignature)
	if err != nil {
		t.Errorf("Expected valid signature, got error: %v", err)
	}
}

// TestValidateSignature_InvalidSignature tests rejection of invalid signatures
func TestValidateSignature_InvalidSignature(t *testing.T) {
	secret := "It's a Secret to Everybody"
	payload := []byte("Hello, World!")
	invalidSignature := "sha256=0000000000000000000000000000000000000000000000000000000000000000"

	err := ValidateSignature(payload, secret, invalidSignature)
	if err != ErrInvalidSignature {
		t.Errorf("Expected ErrInvalidSignature, got: %v", err)
	}
}

// TestValidateSignature_MissingSignature tests rejection when signature header is missing
func TestValidateSignature_MissingSignature(t *testing.T) {
	secret := "It's a Secret to Everybody"
	payload := []byte("Hello, World!")

	err := ValidateSignature(payload, secret, "")
	if err != ErrMissingSignature {
		t.Errorf("Expected ErrMissingSignature, got: %v", err)
	}
}

// TestValidateSignature_WrongSecret tests rejection when wrong secret is used
func TestValidateSignature_WrongSecret(t *testing.T) {
	payload := []byte("Hello, World!")
	correctSignature := "sha256=757107ea0eb2509fc211221cce984b8a37570b6d7586c22c46f4379c8b043e17"
	wrongSecret := "Wrong Secret"

	err := ValidateSignature(payload, wrongSecret, correctSignature)
	if err != ErrInvalidSignature {
		t.Errorf("Expected ErrInvalidSignature when using wrong secret, got: %v", err)
	}
}

// TestValidateSignature_ModifiedPayload tests rejection when payload is modified
func TestValidateSignature_ModifiedPayload(t *testing.T) {
	secret := "It's a Secret to Everybody"
	// Signature is for "Hello, World!"
	signature := "sha256=757107ea0eb2509fc211221cce984b8a37570b6d7586c22c46f4379c8b043e17"
	// But we send a different payload
	modifiedPayload := []byte("Hello, World! Modified")

	err := ValidateSignature(modifiedPayload, secret, signature)
	if err != ErrInvalidSignature {
		t.Errorf("Expected ErrInvalidSignature for modified payload, got: %v", err)
	}
}

// TestComputeSignature tests signature computation
func TestComputeSignature(t *testing.T) {
	secret := "It's a Secret to Everybody"
	payload := []byte("Hello, World!")
	expectedHash := "757107ea0eb2509fc211221cce984b8a37570b6d7586c22c46f4379c8b043e17"
	expectedSignature := "sha256=757107ea0eb2509fc211221cce984b8a37570b6d7586c22c46f4379c8b043e17"

	signature, hexHash := ComputeSignature(payload, secret)

	if hexHash != expectedHash {
		t.Errorf("Expected hash %s, got %s", expectedHash, hexHash)
	}

	if signature != expectedSignature {
		t.Errorf("Expected signature %s, got %s", expectedSignature, signature)
	}
}

// TestParseSignatureHeader tests parsing of signature headers
func TestParseSignatureHeader(t *testing.T) {
	tests := []struct {
		name          string
		header        string
		wantAlgorithm string
		wantHash      string
		wantErr       bool
	}{
		{
			name:          "Valid SHA256 signature",
			header:        "sha256=757107ea0eb2509fc211221cce984b8a37570b6d7586c22c46f4379c8b043e17",
			wantAlgorithm: "sha256",
			wantHash:      "757107ea0eb2509fc211221cce984b8a37570b6d7586c22c46f4379c8b043e17",
			wantErr:       false,
		},
		{
			name:          "Invalid format - no equals sign",
			header:        "sha256",
			wantAlgorithm: "",
			wantHash:      "",
			wantErr:       true,
		},
		{
			name:          "Invalid format - empty string",
			header:        "",
			wantAlgorithm: "",
			wantHash:      "",
			wantErr:       true,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			algorithm, hash, err := ParseSignatureHeader(tt.header)

			if (err != nil) != tt.wantErr {
				t.Errorf("ParseSignatureHeader() error = %v, wantErr %v", err, tt.wantErr)
				return
			}

			if algorithm != tt.wantAlgorithm {
				t.Errorf("ParseSignatureHeader() algorithm = %v, want %v", algorithm, tt.wantAlgorithm)
			}

			if hash != tt.wantHash {
				t.Errorf("ParseSignatureHeader() hash = %v, want %v", hash, tt.wantHash)
			}
		})
	}
}

// TestValidateSignature_UnicodePayload tests validation with unicode characters
func TestValidateSignature_UnicodePayload(t *testing.T) {
	secret := "test-secret"
	payload := []byte("Hello, 世界! 🌍")

	// First compute the expected signature
	expectedSignature, _ := ComputeSignature(payload, secret)

	// Then validate it
	err := ValidateSignature(payload, secret, expectedSignature)
	if err != nil {
		t.Errorf("Expected valid signature for unicode payload, got error: %v", err)
	}
}

// TestValidateSignature_EmptyPayload tests validation with empty payload
func TestValidateSignature_EmptyPayload(t *testing.T) {
	secret := "test-secret"
	payload := []byte("")

	// Compute signature for empty payload
	expectedSignature, _ := ComputeSignature(payload, secret)

	// Validate it
	err := ValidateSignature(payload, secret, expectedSignature)
	if err != nil {
		t.Errorf("Expected valid signature for empty payload, got error: %v", err)
	}
}

// TestValidateSignature_LargePayload tests validation with large payload
func TestValidateSignature_LargePayload(t *testing.T) {
	secret := "test-secret"
	// Create a large payload
	payload := make([]byte, 1024*1024) // 1MB
	for i := range payload {
		payload[i] = byte(i % 256)
	}

	// Compute signature for large payload
	expectedSignature, _ := ComputeSignature(payload, secret)

	// Validate it
	err := ValidateSignature(payload, secret, expectedSignature)
	if err != nil {
		t.Errorf("Expected valid signature for large payload, got error: %v", err)
	}
}
