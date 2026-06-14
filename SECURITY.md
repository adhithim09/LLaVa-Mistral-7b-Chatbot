# Security Policy

We take security seriously at Converso. This document outlines how to report vulnerabilities, what versions are supported, and our security practices.

## Supported Versions

We actively update and patch the latest version of the chatbot.

| Version | Supported          |
| ------- | ------------------ |
| 1.x     | :white_check_mark: |
| < 1.0   | :x:                |

---

## Reporting a Vulnerability

If you discover a security vulnerability, please do **not** open a public issue. Instead, report it privately following these steps:

1. Send an email to the maintainers at `support@converso-chatbot.example.com` (or contact us through private channels specified by repository managers).
2. Include a detailed description of the vulnerability, including:
   * Steps to reproduce or proof-of-concept (PoC).
   * Potential impact on user data or systems.
   * Environment details (OS, Python version, model size).

We will acknowledge receipt of your report within 48 hours and provide updates on resolution progress.

---

## Secure Practices

We enforce several policies to keep Converso secure:
* **Encryption at Rest**: Sensitive database records are encrypted using AES symmetric keys.
* **No Secret Commits**: Our CI system runs Gitleaks on all pull requests to block secret leakage.
* **Dependency Auditing**: Safety scanning automatically runs on PR builds.
