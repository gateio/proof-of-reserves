package main

import (
	"fmt"
	"log"
	"net/http"
	"os"

	"gate-zkmerkle-proof/webhook"
)

func main() {
	// Check if the webhook secret is configured
	secret := os.Getenv("WEBHOOK_SECRET")
	if secret == "" {
		log.Println("WARNING: WEBHOOK_SECRET environment variable is not set")
		log.Println("Please set it before running the server:")
		log.Println("  export WEBHOOK_SECRET='your-secret-token'")
		os.Exit(1)
	}

	// Create a new HTTP mux
	mux := http.NewServeMux()

	// Register the webhook handler
	mux.HandleFunc("/webhook", webhook.WebhookHandler)

	// Add a health check endpoint
	mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		fmt.Fprintf(w, "OK")
	})

	// Add a root endpoint with instructions
	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Content-Type", "text/html")
		fmt.Fprintf(w, `
<!DOCTYPE html>
<html>
<head>
    <title>GitHub Webhook Server</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }
        pre { background: #f4f4f4; padding: 15px; border-radius: 5px; overflow-x: auto; }
    </style>
</head>
<body>
    <h1>GitHub Webhook Server</h1>
    <p>This server is running and ready to receive GitHub webhooks.</p>
    
    <h2>Configuration</h2>
    <ul>
        <li>Webhook endpoint: <code>/webhook</code></li>
        <li>Health check: <code>/health</code></li>
        <li>Secret configured: ✓</li>
    </ul>
    
    <h2>Setup Instructions</h2>
    <ol>
        <li>Go to your GitHub repository settings</li>
        <li>Navigate to Webhooks → Add webhook</li>
        <li>Set Payload URL to: <code>https://your-domain.com/webhook</code></li>
        <li>Set Content type to: <code>application/json</code></li>
        <li>Set Secret to the same value as your WEBHOOK_SECRET environment variable</li>
        <li>Select the events you want to receive</li>
        <li>Click "Add webhook"</li>
    </ol>
    
    <h2>Testing</h2>
    <p>Test your webhook using curl:</p>
    <pre>
SECRET="your-secret-token"
PAYLOAD='{"test": "data"}'
SIGNATURE="sha256=$(echo -n "$PAYLOAD" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)"

curl -X POST http://localhost:8080/webhook \
  -H "Content-Type: application/json" \
  -H "X-Hub-Signature-256: $SIGNATURE" \
  -d "$PAYLOAD"
    </pre>
    
    <h2>Security</h2>
    <p>This server validates all webhook signatures using HMAC-SHA256 to ensure:</p>
    <ul>
        <li>Webhooks are genuinely from GitHub</li>
        <li>Payloads have not been tampered with</li>
        <li>Protection against man-in-the-middle attacks</li>
    </ul>
</body>
</html>
		`)
	})

	// Get the port from environment variable or use default
	port := os.Getenv("PORT")
	if port == "" {
		port = "8080"
	}
	addr := ":" + port

	// Create a secure server with appropriate timeouts
	server := webhook.SecureWebhookServer(addr, mux)

	// Start the server
	log.Printf("Starting GitHub webhook server on %s", addr)
	log.Printf("Webhook endpoint: http://localhost%s/webhook", addr)
	log.Printf("Health check: http://localhost%s/health", addr)
	log.Fatal(server.ListenAndServe())
}
