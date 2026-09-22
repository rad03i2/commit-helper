# Security Policy

Commit Helper is an offline text-processing utility. It does not use the network, execute Git commands, modify repositories, or evaluate commit-message content.

## Supported versions
Security fixes target the latest release on `main`.

## Reporting
Please report suspected vulnerabilities privately through GitHub's security reporting features when available. Do not include real credentials, tokens, or other sensitive data in public issues.

## Scope
Files supplied through `--file` are read as UTF-8 text. Treat untrusted paths according to your operating system's normal file-access rules. Commit Helper does not provide sandboxing and should not be run with elevated privileges unnecessarily.
