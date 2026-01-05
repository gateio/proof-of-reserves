# Webhook Security Best Practices

## Overview

This document outlines security best practices for implementing and using GitHub webhooks with this project. Proper webhook security is critical to prevent unauthorized access and ensure the integrity of your system.

## Signature Validation

### Why Validate Signatures?

Webhook signature validation ensures that:

1. **Authenticity**: The webhook payload was actually sent by GitHub, not a malicious third party
2. **Integrity**: The payload has not been modified or tampered with during transmission
3. **Non-repudiation**: You have cryptographic proof of the payload's origin

### How Signature Validation Works

1. **GitHub's Process**:
   - GitHub creates an HMAC-SHA256 hash of the payload using your secret token
   - The hash is sent in the `X-Hub-Signature-256` header
   - Format: `sha256=<hex_encoded_hash>`

2. **Your Server's Process**:
   - Receive the webhook payload and signature header
   - Compute your own HMAC-SHA256 hash using the same secret
   - Compare the hashes using constant-time comparison
   - Accept only if they match exactly

### Example Code

```go
err := webhook.ValidateSignature(payloadBody, secretToken, signatureHeader)
if err == webhook.ErrMissingSignature {
    // No signature provided - reject
    http.Error(w, "Missing signature", http.StatusForbidden)
    return
}
if err == webhook.ErrInvalidSignature {
    // Invalid signature - possible attack
    log.Printf("SECURITY WARNING: Invalid webhook signature from %s", r.RemoteAddr)
    http.Error(w, "Invalid signature", http.StatusForbidden)
    return
}
// Signature valid - safe to process
```

## Secret Token Management

### Generating Secure Secrets

Use a cryptographically secure random string with high entropy:

```bash
# Good: 256 bits of entropy
openssl rand -hex 32

# Good: Base64 encoded random bytes
openssl rand -base64 32

# Bad: Predictable or short secrets
# DON'T USE: "password123", "secret", etc.
```

### Storing Secrets Securely

**DO:**
- ✅ Use environment variables
- ✅ Use secret management services (AWS Secrets Manager, HashiCorp Vault, etc.)
- ✅ Encrypt secrets at rest
- ✅ Limit access to secrets using IAM/RBAC
- ✅ Rotate secrets periodically

**DON'T:**
- ❌ Hardcode secrets in source code
- ❌ Commit secrets to version control
- ❌ Store secrets in plain text files
- ❌ Share secrets via email or chat
- ❌ Log secrets in application logs

### Environment Variables Example

```bash
# Set in your environment
export WEBHOOK_SECRET="your-cryptographically-random-secret-here"

# Or in a .env file (add to .gitignore!)
echo 'WEBHOOK_SECRET=your-secret-here' > .env.local

# Load in your application
source .env.local
go run main.go
```

### Secret Rotation

Rotate webhook secrets periodically:

1. Generate a new secret token
2. Update the secret in GitHub webhook settings
3. Update the secret in your server configuration
4. Deploy the changes
5. Monitor for any validation failures

## Network Security

### Use HTTPS

**Always** use HTTPS for webhook endpoints:

```go
// DON'T: Insecure HTTP
http.ListenAndServe(":80", handler)

// DO: Secure HTTPS with TLS
http.ListenAndServeTLS(":443", "cert.pem", "key.pem", handler)
```

### Configure GitHub Webhook Settings

In your GitHub webhook configuration:

1. **Payload URL**: Use HTTPS URLs only
2. **Content type**: Set to `application/json`
3. **Secret**: Always configure a secret token
4. **SSL verification**: Keep enabled (default)
5. **Events**: Only subscribe to events you need

### Firewall Configuration

Restrict webhook endpoint access:

```bash
# Example: Allow only GitHub webhook IPs
# GitHub publishes their webhook IPs in the Meta API
# https://api.github.com/meta

# Example firewall rule (iptables)
iptables -A INPUT -p tcp --dport 443 -s 192.30.252.0/22 -j ACCEPT
iptables -A INPUT -p tcp --dport 443 -j DROP
```

## Application Security

### Validate All Inputs

After signature validation, validate the payload content:

```go
// Validate signature first
if err := webhook.ValidateSignature(body, secret, signature); err != nil {
    return err
}

// Then validate payload structure
var payload WebhookPayload
if err := json.Unmarshal(body, &payload); err != nil {
    return fmt.Errorf("invalid JSON: %w", err)
}

// Validate business logic constraints
if payload.Repository == "" {
    return errors.New("missing repository field")
}
```

### Rate Limiting

Implement rate limiting to prevent abuse:

```go
import "golang.org/x/time/rate"

var limiter = rate.NewLimiter(rate.Limit(10), 20) // 10 req/s, burst of 20

func webhookHandler(w http.ResponseWriter, r *http.Request) {
    if !limiter.Allow() {
        http.Error(w, "Rate limit exceeded", http.StatusTooManyRequests)
        return
    }
    // Process webhook...
}
```

### Request Size Limits

Limit request body size to prevent memory exhaustion:

```go
// Limit to 1MB
r.Body = http.MaxBytesReader(w, r.Body, 1<<20)

body, err := io.ReadAll(r.Body)
if err != nil {
    http.Error(w, "Request too large", http.StatusRequestEntityTooLarge)
    return
}
```

### Timeout Configuration

Use appropriate timeouts in your server:

```go
server := &http.Server{
    Addr:         ":8080",
    Handler:      handler,
    ReadTimeout:  5 * time.Second,   // Time to read request
    WriteTimeout: 10 * time.Second,  // Time to write response
    IdleTimeout:  120 * time.Second, // Time for keep-alive
}
```

## Monitoring and Logging

### Log Security Events

Log all security-relevant events:

```go
// Log successful validations (info level)
log.Printf("Valid webhook received from %s, event: %s", 
    r.RemoteAddr, r.Header.Get("X-GitHub-Event"))

// Log validation failures (warning level)
log.Printf("WARNING: Invalid signature from %s", r.RemoteAddr)

// Log missing signatures (warning level)
log.Printf("WARNING: Missing signature header from %s", r.RemoteAddr)
```

### Monitor for Attacks

Set up alerts for:

- Multiple invalid signature attempts
- Missing signature headers
- Unusual traffic patterns
- Requests from unexpected IP addresses

### Audit Trail

Maintain an audit trail of webhook deliveries:

```go
type WebhookLog struct {
    Timestamp   time.Time
    RemoteAddr  string
    Event       string
    Signature   string
    Valid       bool
    PayloadHash string
}

// Store in database or logging system
auditLog := WebhookLog{
    Timestamp:   time.Now(),
    RemoteAddr:  r.RemoteAddr,
    Event:       r.Header.Get("X-GitHub-Event"),
    Valid:       validationPassed,
    PayloadHash: computeHash(payload),
}
```

## Attack Prevention

### Timing Attacks

Always use constant-time comparison for signatures:

```go
// ✅ GOOD: Constant-time comparison (implemented in ValidateSignature)
if !hmac.Equal([]byte(expected), []byte(received)) {
    return errors.New("invalid signature")
}

// ❌ BAD: Vulnerable to timing attacks
if expected == received {
    return nil
}
```

### Replay Attacks

Implement replay attack prevention:

```go
// Check webhook delivery timestamp
delivered := r.Header.Get("X-GitHub-Delivery")
timestamp := r.Header.Get("X-Hub-Signature")

// Reject old deliveries (e.g., older than 5 minutes)
const maxAge = 5 * time.Minute
if time.Since(deliveryTime) > maxAge {
    return errors.New("webhook delivery too old")
}

// Store and check delivery IDs to prevent replays
if alreadyProcessed(delivered) {
    return errors.New("duplicate delivery")
}
```

### Man-in-the-Middle Attacks

Protect against MITM attacks:

1. **Use HTTPS**: Encrypts data in transit
2. **Validate Signatures**: Ensures payload integrity
3. **Certificate Pinning**: For additional security (advanced)

## Compliance and Best Practices

### OWASP Guidelines

Follow OWASP API Security Top 10:

1. **Broken Object Level Authorization**: Validate all webhook actions
2. **Broken Authentication**: Always validate signatures
3. **Excessive Data Exposure**: Log only necessary data
4. **Lack of Resources & Rate Limiting**: Implement rate limiting
5. **Broken Function Level Authorization**: Check user permissions

### Regular Security Audits

Perform regular security reviews:

- Review access logs monthly
- Test signature validation quarterly
- Rotate secrets annually (or after incidents)
- Update dependencies regularly
- Scan for vulnerabilities with tools

### Incident Response

Have an incident response plan:

1. **Detection**: Monitor for suspicious activity
2. **Containment**: Disable compromised webhooks
3. **Investigation**: Review logs and audit trail
4. **Recovery**: Rotate secrets, update configurations
5. **Lessons Learned**: Document and improve

## Testing Security

### Test Invalid Signatures

```go
func TestInvalidSignature(t *testing.T) {
    payload := []byte("test")
    secret := "correct-secret"
    wrongSignature := "sha256=wrong"
    
    err := webhook.ValidateSignature(payload, secret, wrongSignature)
    if err != webhook.ErrInvalidSignature {
        t.Error("Should reject invalid signature")
    }
}
```

### Test Missing Signatures

```go
func TestMissingSignature(t *testing.T) {
    payload := []byte("test")
    secret := "secret"
    
    err := webhook.ValidateSignature(payload, secret, "")
    if err != webhook.ErrMissingSignature {
        t.Error("Should reject missing signature")
    }
}
```

### Penetration Testing

Consider professional penetration testing for production systems.

## Additional Resources

- [GitHub Webhook Security](https://docs.github.com/en/developers/webhooks-and-events/webhooks/securing-your-webhooks)
- [OWASP API Security](https://owasp.org/www-project-api-security/)
- [NIST Cryptographic Standards](https://csrc.nist.gov/publications)

## Support

For security concerns or to report vulnerabilities, see [SECURITY.md](../SECURITY.md).
