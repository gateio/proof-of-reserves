package webhook

import (
	"bytes"
	"net/http"
	"net/http/httptest"
	"os"
	"testing"
)

func TestWebhookHandler_ValidRequest(t *testing.T) {
	// Set up test environment
	secret := "test-secret"
	os.Setenv("WEBHOOK_SECRET", secret)
	defer os.Unsetenv("WEBHOOK_SECRET")

	// Create test payload
	payload := []byte(`{"action":"opened","number":1}`)
	signature, _ := ComputeSignature(payload, secret)

	// Create request
	req := httptest.NewRequest(http.MethodPost, "/webhook", bytes.NewReader(payload))
	req.Header.Set("X-Hub-Signature-256", signature)
	req.Header.Set("Content-Type", "application/json")

	// Record response
	w := httptest.NewRecorder()

	// Call handler
	WebhookHandler(w, req)

	// Check response
	if w.Code != http.StatusOK {
		t.Errorf("Expected status %d, got %d", http.StatusOK, w.Code)
	}
}

func TestWebhookHandler_InvalidSignature(t *testing.T) {
	// Set up test environment
	secret := "test-secret"
	os.Setenv("WEBHOOK_SECRET", secret)
	defer os.Unsetenv("WEBHOOK_SECRET")

	// Create test payload with wrong signature
	payload := []byte(`{"action":"opened","number":1}`)
	wrongSignature := "sha256=0000000000000000000000000000000000000000000000000000000000000000"

	// Create request
	req := httptest.NewRequest(http.MethodPost, "/webhook", bytes.NewReader(payload))
	req.Header.Set("X-Hub-Signature-256", wrongSignature)
	req.Header.Set("Content-Type", "application/json")

	// Record response
	w := httptest.NewRecorder()

	// Call handler
	WebhookHandler(w, req)

	// Check response
	if w.Code != http.StatusForbidden {
		t.Errorf("Expected status %d, got %d", http.StatusForbidden, w.Code)
	}
}

func TestWebhookHandler_MissingSignature(t *testing.T) {
	// Set up test environment
	secret := "test-secret"
	os.Setenv("WEBHOOK_SECRET", secret)
	defer os.Unsetenv("WEBHOOK_SECRET")

	// Create test payload without signature header
	payload := []byte(`{"action":"opened","number":1}`)

	// Create request
	req := httptest.NewRequest(http.MethodPost, "/webhook", bytes.NewReader(payload))
	req.Header.Set("Content-Type", "application/json")
	// Note: No X-Hub-Signature-256 header

	// Record response
	w := httptest.NewRecorder()

	// Call handler
	WebhookHandler(w, req)

	// Check response
	if w.Code != http.StatusForbidden {
		t.Errorf("Expected status %d, got %d", http.StatusForbidden, w.Code)
	}
}

func TestWebhookHandler_WrongMethod(t *testing.T) {
	// Create request with GET method
	req := httptest.NewRequest(http.MethodGet, "/webhook", nil)

	// Record response
	w := httptest.NewRecorder()

	// Call handler
	WebhookHandler(w, req)

	// Check response
	if w.Code != http.StatusMethodNotAllowed {
		t.Errorf("Expected status %d, got %d", http.StatusMethodNotAllowed, w.Code)
	}
}

func TestWebhookHandler_MissingSecret(t *testing.T) {
	// Ensure WEBHOOK_SECRET is not set
	os.Unsetenv("WEBHOOK_SECRET")

	// Create test payload
	payload := []byte(`{"action":"opened","number":1}`)
	signature := "sha256=somehash"

	// Create request
	req := httptest.NewRequest(http.MethodPost, "/webhook", bytes.NewReader(payload))
	req.Header.Set("X-Hub-Signature-256", signature)
	req.Header.Set("Content-Type", "application/json")

	// Record response
	w := httptest.NewRecorder()

	// Call handler
	WebhookHandler(w, req)

	// Check response
	if w.Code != http.StatusInternalServerError {
		t.Errorf("Expected status %d, got %d", http.StatusInternalServerError, w.Code)
	}
}

func TestWebhookHandler_InvalidJSON(t *testing.T) {
	// Set up test environment
	secret := "test-secret"
	os.Setenv("WEBHOOK_SECRET", secret)
	defer os.Unsetenv("WEBHOOK_SECRET")

	// Create invalid JSON payload
	payload := []byte(`{invalid json}`)
	signature, _ := ComputeSignature(payload, secret)

	// Create request
	req := httptest.NewRequest(http.MethodPost, "/webhook", bytes.NewReader(payload))
	req.Header.Set("X-Hub-Signature-256", signature)
	req.Header.Set("Content-Type", "application/json")

	// Record response
	w := httptest.NewRecorder()

	// Call handler
	WebhookHandler(w, req)

	// Check response - signature is valid, but JSON is invalid
	if w.Code != http.StatusBadRequest {
		t.Errorf("Expected status %d, got %d", http.StatusBadRequest, w.Code)
	}
}

func TestSecureWebhookServer(t *testing.T) {
	mux := http.NewServeMux()
	mux.HandleFunc("/webhook", WebhookHandler)

	server := SecureWebhookServer(":8080", mux)

	if server.Addr != ":8080" {
		t.Errorf("Expected server address :8080, got %s", server.Addr)
	}

	if server.Handler == nil {
		t.Error("Expected handler to be set")
	}

	if server.ReadTimeout == 0 {
		t.Error("Expected ReadTimeout to be set")
	}

	if server.WriteTimeout == 0 {
		t.Error("Expected WriteTimeout to be set")
	}

	if server.IdleTimeout == 0 {
		t.Error("Expected IdleTimeout to be set")
	}
}
