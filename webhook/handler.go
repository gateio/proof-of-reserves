package webhook

import (
	"encoding/json"
	"io"
	"log"
	"net/http"
	"os"
	"time"
)

// WebhookHandler is an HTTP handler that validates GitHub webhook signatures
// and processes the webhook payload.
//
// Example usage:
//
//	http.HandleFunc("/webhook", webhook.WebhookHandler)
//	log.Fatal(http.ListenAndServe(":8080", nil))
func WebhookHandler(w http.ResponseWriter, r *http.Request) {
	// Only accept POST requests
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	// Read the request body
	body, err := io.ReadAll(r.Body)
	if err != nil {
		log.Printf("Error reading request body: %v", err)
		http.Error(w, "Error reading request body", http.StatusBadRequest)
		return
	}
	defer r.Body.Close()

	// Get the signature from the header
	signature := r.Header.Get("X-Hub-Signature-256")

	// Get the secret token from environment variable
	secret := os.Getenv("WEBHOOK_SECRET")
	if secret == "" {
		log.Printf("WEBHOOK_SECRET environment variable not set")
		http.Error(w, "Server configuration error", http.StatusInternalServerError)
		return
	}

	// Validate the signature
	err = ValidateSignature(body, secret, signature)
	if err == ErrMissingSignature {
		log.Printf("Missing signature header")
		http.Error(w, "x-hub-signature-256 header is missing", http.StatusForbidden)
		return
	}
	if err == ErrInvalidSignature {
		log.Printf("Invalid signature")
		http.Error(w, "Request signatures didn't match", http.StatusForbidden)
		return
	}
	if err != nil {
		log.Printf("Error validating signature: %v", err)
		http.Error(w, "Error validating signature", http.StatusInternalServerError)
		return
	}

	// Signature is valid, process the webhook payload
	var payload map[string]interface{}
	if err := json.Unmarshal(body, &payload); err != nil {
		log.Printf("Error parsing JSON payload: %v", err)
		http.Error(w, "Invalid JSON payload", http.StatusBadRequest)
		return
	}

	// Log successful webhook receipt
	log.Printf("Received valid webhook payload: %d bytes", len(body))

	// Process the webhook payload here
	// For example, you might want to check the event type:
	// eventType := r.Header.Get("X-GitHub-Event")

	// Send success response
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("Webhook received and validated successfully"))
}

// SecureWebhookServer creates and configures an HTTP server for webhook handling.
// The server is configured with appropriate timeouts and settings for production use.
//
// Args:
//   - addr: the address to listen on (e.g., ":8080")
//   - handler: the HTTP handler to use for webhook requests
//
// Returns:
//   - *http.Server: configured HTTP server ready to start
//
// Example:
//
//	mux := http.NewServeMux()
//	mux.HandleFunc("/webhook", webhook.WebhookHandler)
//	server := webhook.SecureWebhookServer(":8080", mux)
//	log.Fatal(server.ListenAndServe())
func SecureWebhookServer(addr string, handler http.Handler) *http.Server {
	return &http.Server{
		Addr:    addr,
		Handler: handler,
		// Add reasonable timeouts to prevent slowloris attacks
		ReadTimeout:  5 * time.Second,
		WriteTimeout: 10 * time.Second,
		IdleTimeout:  120 * time.Second,
	}
}
