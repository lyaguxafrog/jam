---
title: Jam lists
---

# What is Jam lists?
Jam lists are optional modules for managing white and black lists.

## What is a Blacklist?
A **blacklist** is a list of invalidated tokens. Even if a token has not yet expired (i.e., `exp` claim is still valid),
it can be manually added to the blacklist to prevent further use.

### Common use cases:
* A user logs out — their token is blacklisted.
* A token is compromised — it must be immediately revoked.
* A user's access rights change — old tokens may no longer be valid.

## What is a Whitelist?
A **whitelist** is a list of explicitly approved tokens.
Only tokens that are present in this list are considered valid. All others are automatically rejected.

### Common use cases:
* High-security environments where only verified sessions should work.
* Limiting the number of active sessions per user.
* Centralized control over all active tokens.

## When to Use Blacklist vs. Whitelist
| Scenario                                                | Recommended List Type |
|---------------------------------------------------------|----------------------:|
| Standard login/logout behavior                          |             Blacklist |
| High-security systems with strict session control       |             Whitelist |
| Immediate token revocation needed                       |             Blacklist |
| Tokens are rarely issued and must be tightly controlled |             Whitelist |
| Scalable APIs with minimal storage overhead             |   Blacklist (or none) |