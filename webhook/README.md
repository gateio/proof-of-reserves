# GitHub Webhook Signature Validation

This package provides secure validation of GitHub webhook signatures using HMAC-SHA256. It implements the verification method recommended by GitHub to ensure webhook deliveries are authentic and have not been tampered with.

## Features

- **HMAC-SHA256 Validation**: Validates webhook payloads using GitHub's recommended signature method
- **Constant-Time Comparison**: Uses `hmac.Equal()` to prevent timing attacks
- **Easy Integration**: Simple API for validating signatures in your webhook handlers
- **Complete Example Server**: Includes a production-ready webhook server implementation
- **Comprehensive Tests**: Extensive test coverage including edge cases

## Quick Start

### Basic Usage

```go
package main

import (
    "io"
    "net/http"
    "os"
    "gate-zkmerkle-proof/webhook"
)

func handleWebhook(w http.ResponseWriter, r *http.Request) {
    // Read the request body
    body, err := io.ReadAll(r.Body)
    if err != nil {
        http.Error(w, "Error reading request body", http.StatusBadRequest)
        return
    }
    defer r.Body.Close()

    // Get the signature from the header
    signature := r.Header.Get("X-Hub-Signature-256")

    // Get your webhook secret from environment variable
    secret := os.Getenv("WEBHOOK_SECRET")

    // Validate the signature
    err = webhook.ValidateSignature(body, secret, signature)
    if err != nil {
        http.Error(w, "Invalid signature", http.StatusForbidden)
        return
    }

    // Signature is valid, process the webhook
    w.WriteHeader(http.StatusOK)
    w.Write([]byte("Webhook validated successfully"))
}
```

### Using the Built-in Handler

The package includes a ready-to-use webhook handler:

```go
package main

import (
    "log"
    "net/http"
    "gate-zkmerkle-proof/webhook"
)

func main() {
    http.HandleFunc("/webhook", webhook.WebhookHandler)
    log.Fatal(http.ListenAndServe(":8080", nil))
}
```

### Production Server with Security Settings

For production use, use the `SecureWebhookServer` function which includes appropriate timeouts:

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
    
    server := webhook.SecureWebhookServer(":8080", mux)
    log.Printf("Starting webhook server on %s", server.Addr)
    log.Fatal(server.ListenAndServe())
}
```

## Configuration

### Setting Up Your Webhook Secret

1. **Generate a Secret Token**: Create a random string with high entropy. You can use:
   ```bash
   openssl rand -hex 32
   ```

2. **Store the Secret Securely**: 
   - **Environment Variable** (recommended):
     ```bash
     export WEBHOOK_SECRET="your-secret-token-here"
     ```
   - **Secret Manager**: Use AWS Secrets Manager, HashiCorp Vault, or similar
   - **Never** hardcode the secret in your application or commit it to version control

3. **Configure GitHub**:
   - Go to your repository Settings → Webhooks
   - Add or edit your webhook
   - Under "Secret", enter the same secret token
   - Select "application/json" as the content type
   - Choose the events you want to receive

## Security Best Practices

### 1. Always Validate Signatures

Never process webhook payloads without validating the signature first:

```go
// ✅ GOOD
err := webhook.ValidateSignature(body, secret, signature)
if err != nil {
    return // Reject the request
}
// Process the webhook

// ❌ BAD - Don't skip validation
// Process the webhook without checking signature
```

### 2. Use Constant-Time Comparison

The package automatically uses `hmac.Equal()` for constant-time comparison to prevent timing attacks. Never use regular string comparison:

```go
// ✅ GOOD - Uses hmac.Equal() internally
err := webhook.ValidateSignature(body, secret, signature)

// ❌ BAD - Vulnerable to timing attacks
if signature == expectedSignature {
    // ...
}
```

### 3. Secure Secret Storage

- **Never** hardcode secrets in your code
- **Never** commit secrets to version control
- Use environment variables or secret management services
- Rotate secrets periodically

### 4. Handle UTF-8 Properly

GitHub webhook payloads can contain Unicode characters. This package handles UTF-8 correctly by default:

```go
// Works correctly with Unicode
payload := []byte("Hello, 世界! 🌍")
err := webhook.ValidateSignature(payload, secret, signature)
```

### 5. Use HTTPS

Always use HTTPS for your webhook endpoint to prevent man-in-the-middle attacks. GitHub will only deliver webhooks to HTTPS endpoints in production.

## API Reference

### Functions

#### ValidateSignature

```go
func ValidateSignature(payloadBody []byte, secretToken string, signatureHeader string) error
```

Validates that the payload was sent from GitHub by validating the HMAC-SHA256 signature.

**Parameters:**
- `payloadBody`: The raw request body bytes
- `secretToken`: Your webhook secret token
- `signatureHeader`: The value of the `X-Hub-Signature-256` header

**Returns:**
- `nil` if the signature is valid
- `ErrMissingSignature` if the signature header is missing
- `ErrInvalidSignature` if the signature doesn't match

**Example:**
```go
err := webhook.ValidateSignature(body, secret, signature)
if err == webhook.ErrMissingSignature {
    // Handle missing signature
} else if err == webhook.ErrInvalidSignature {
    // Handle invalid signature
}
```

#### ComputeSignature

```go
func ComputeSignature(payloadBody []byte, secretToken string) (signature string, hexHash string)
```

Computes the HMAC-SHA256 signature for a payload. Primarily used for testing and debugging.

**Parameters:**
- `payloadBody`: The payload to sign
- `secretToken`: The secret token to use for signing

**Returns:**
- `signature`: The full signature in the format `"sha256=<hex>"`
- `hexHash`: The hex-encoded hash without the `"sha256="` prefix

**Example:**
```go
signature, hash := webhook.ComputeSignature([]byte("Hello, World!"), "my-secret")
// signature: "sha256=757107ea0eb2509fc211221cce984b8a37570b6d7586c22c46f4379c8b043e17"
// hash: "757107ea0eb2509fc211221cce984b8a37570b6d7586c22c46f4379c8b043e17"
```

#### ParseSignatureHeader

```go
func ParseSignatureHeader(signatureHeader string) (algorithm string, hash string, err error)
```

Extracts the algorithm and hash from a signature header.

**Parameters:**
- `signatureHeader`: The signature header value (e.g., `"sha256=abc123..."`)

**Returns:**
- `algorithm`: The hashing algorithm (e.g., `"sha256"`)
- `hash`: The hex-encoded hash value
- `err`: An error if parsing fails

#### WebhookHandler

```go
func WebhookHandler(w http.ResponseWriter, r *http.Request)
```

An HTTP handler that validates GitHub webhook signatures and processes the payload.

**Features:**
- Validates the signature before processing
- Returns appropriate HTTP status codes
- Logs validation results
- Reads secret from `WEBHOOK_SECRET` environment variable

#### SecureWebhookServer

```go
func SecureWebhookServer(addr string, handler http.Handler) *http.Server
```

Creates and configures an HTTP server with security settings appropriate for production use.

**Parameters:**
- `addr`: The address to listen on (e.g., `":8080"`)
- `handler`: The HTTP handler to use

**Returns:**
- Configured `*http.Server` with appropriate timeouts

## Testing

### Running Tests

```bash
cd webhook
go test -v
```

### Testing Your Webhook Implementation

GitHub provides test values you can use to verify your implementation:

**Test Values:**
- Secret: `It's a Secret to Everybody`
- Payload: `Hello, World!`
- Expected Hash: `757107ea0eb2509fc211221cce984b8a37570b6d7586c22c46f4379c8b043e17`
- Expected Signature: `sha256=757107ea0eb2509fc211221cce984b8a37570b6d7586c22c46f4379c8b043e17`

**Test in Go:**
```go
secret := "It's a Secret to Everybody"
payload := []byte("Hello, World!")
signature := "sha256=757107ea0eb2509fc211221cce984b8a37570b6d7586c22c46f4379c8b043e17"

err := webhook.ValidateSignature(payload, secret, signature)
if err != nil {
    log.Fatal("Validation failed!")
}
log.Println("Validation successful!")
```

### Testing with curl

You can test your webhook endpoint using curl:

```bash
# Generate a signature
SECRET="your-secret-token"
PAYLOAD='{"test": "data"}'
SIGNATURE="sha256=$(echo -n "$PAYLOAD" | openssl dgst -sha256 -hmac "$SECRET" | cut -d' ' -f2)"

# Send the request
curl -X POST http://localhost:8080/webhook \
  -H "Content-Type: application/json" \
  -H "X-Hub-Signature-256: $SIGNATURE" \
  -d "$PAYLOAD"
```

## Troubleshooting

### Signature Verification Fails

If signature verification fails, check:

1. **Correct Secret**: Ensure you're using the same secret configured in GitHub
2. **Correct Header**: Use `X-Hub-Signature-256` (not the legacy `X-Hub-Signature`)
3. **Correct Algorithm**: Ensure you're using HMAC-SHA256
4. **Unmodified Payload**: The payload must not be modified before verification
5. **UTF-8 Encoding**: Ensure proper UTF-8 handling if payload contains Unicode

### Missing Signature Header

If you get `ErrMissingSignature`:

1. **Secret Configured**: Make sure you've configured a secret for your webhook in GitHub
2. **Correct Header Name**: Check that GitHub is sending the `X-Hub-Signature-256` header

### Environment Variable Not Set

If you get a server configuration error:

```bash
export WEBHOOK_SECRET="your-secret-token"
```

Or set it in your deployment configuration (Kubernetes, Docker, etc.).

## Examples

See the test files for complete examples:
- `validator_test.go`: Examples of signature validation
- `handler_test.go`: Examples of HTTP handler usage

## References

- [GitHub Webhooks Documentation](https://docs.github.com/en/developers/webhooks-and-events/webhooks/securing-your-webhooks)
- [HMAC-SHA256 RFC](https://tools.ietf.org/html/rfc2104)

## License

This code is part of the gate-zkmerkle-proof project and is licensed under the GPLv3 license.
