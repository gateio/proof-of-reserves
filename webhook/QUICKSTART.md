# Quick Start Guide - GitHub Webhook Signature Validation

This is a quick reference for implementing GitHub webhook signature validation in your Go application.

## 1. Install Dependencies

This package is included in the `gate-zkmerkle-proof` project. No additional dependencies needed beyond the Go standard library.

## 2. Set Your Webhook Secret

```bash
# Generate a secure secret
openssl rand -hex 32

# Set it as an environment variable
export WEBHOOK_SECRET="your-generated-secret-here"
```

## 3. Configure GitHub Webhook

1. Go to your repository → Settings → Webhooks
2. Click "Add webhook"
3. Configure:
   - **Payload URL**: `https://your-domain.com/webhook`
   - **Content type**: `application/json`
   - **Secret**: (paste your secret from step 2)
   - **SSL verification**: Enable (recommended)
   - **Events**: Select what you need
4. Click "Add webhook"

## 4. Basic Implementation

### Option A: Use the Built-in Handler

```go
package main

import (
    "log"
    "net/http"
    "gate-zkmerkle-proof/webhook"
)

func main() {
    // The handler reads WEBHOOK_SECRET from environment
    http.HandleFunc("/webhook", webhook.WebhookHandler)
    log.Fatal(http.ListenAndServe(":8080", nil))
}
```

### Option B: Custom Handler

```go
package main

import (
    "io"
    "log"
    "net/http"
    "os"
    "gate-zkmerkle-proof/webhook"
)

func customWebhookHandler(w http.ResponseWriter, r *http.Request) {
    // Read body
    body, _ := io.ReadAll(r.Body)
    
    // Get signature
    signature := r.Header.Get("X-Hub-Signature-256")
    
    // Validate
    err := webhook.ValidateSignature(body, os.Getenv("WEBHOOK_SECRET"), signature)
    if err != nil {
        http.Error(w, "Invalid signature", http.StatusForbidden)
        return
    }
    
    // Process webhook...
    log.Println("Valid webhook received!")
    w.Write([]byte("OK"))
}

func main() {
    http.HandleFunc("/webhook", customWebhookHandler)
    log.Fatal(http.ListenAndServe(":8080", nil))
}
```

### Option C: Production Server with Security

```go
package main

import (
    "log"
    "net/http"
    "gate-zkmerkle-proof/webhook"
)

func main() {
    mux := http.NewServeMux()
    mux.HandleFunc("/webhook", webhook.WebhookHandler)
    
    // Secure server with timeouts
    server := webhook.SecureWebhookServer(":8080", mux)
    log.Fatal(server.ListenAndServe())
}
```

## 5. Run Your Server

```bash
# Make sure WEBHOOK_SECRET is set
export WEBHOOK_SECRET="your-secret"

# Run your application
go run main.go
```

## 6. Test Your Implementation

### Test with GitHub's Test Values

```bash
# Test with the official GitHub test values
SECRET="It's a Secret to Everybody"
PAYLOAD="Hello, World!"
SIGNATURE="sha256=757107ea0eb2509fc211221cce984b8a37570b6d7586c22c46f4379c8b043e17"

curl -X POST http://localhost:8080/webhook \
  -H "Content-Type: application/json" \
  -H "X-Hub-Signature-256: $SIGNATURE" \
  -d "$PAYLOAD"
```

### Test with Your Own Secret

```bash
# Using your actual secret
SECRET="your-webhook-secret"
PAYLOAD='{"test": "data"}'
SIGNATURE="sha256=$(echo -n "$PAYLOAD" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)"

curl -X POST http://localhost:8080/webhook \
  -H "Content-Type: application/json" \
  -H "X-Hub-Signature-256: $SIGNATURE" \
  -d "$PAYLOAD"
```

## 7. Run the Example Server

```bash
export WEBHOOK_SECRET="your-secret"
cd examples/webhook-server
go run main.go
```

Then visit http://localhost:8080 for instructions and http://localhost:8080/webhook for the endpoint.

## Common Issues

### "Missing signature header"
- Make sure you've configured a secret in GitHub webhook settings
- Check that the header name is exactly `X-Hub-Signature-256`

### "Request signatures didn't match"
- Verify you're using the correct secret
- Ensure the payload isn't being modified before validation
- Check that you're reading the raw body bytes

### "WEBHOOK_SECRET environment variable not set"
- Set the environment variable: `export WEBHOOK_SECRET="your-secret"`
- Or set it in your deployment configuration

## Security Checklist

- ✅ Always validate signatures before processing
- ✅ Use a cryptographically random secret (32+ bytes)
- ✅ Store secrets in environment variables or secret manager
- ✅ Never commit secrets to version control
- ✅ Use HTTPS for your webhook endpoint
- ✅ Enable SSL verification in GitHub
- ✅ Implement rate limiting in production
- ✅ Monitor for failed validation attempts

## Next Steps

- Read the full [README](./README.md) for detailed documentation
- Review [SECURITY.md](./SECURITY.md) for security best practices
- Check out the [example server](../examples/webhook-server/main.go) for a complete implementation

## Need Help?

- Run tests: `cd webhook && go test -v`
- Check logs for validation errors
- Review GitHub's [webhook documentation](https://docs.github.com/en/developers/webhooks-and-events/webhooks/securing-your-webhooks)
