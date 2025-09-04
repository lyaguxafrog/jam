---
title: HOTP vs TOTP
---


## What is OTP?

[OTP](https://en.wikipedia.org/wiki/One-time_password) stands for **One-Time Password**.
It is used for **two-factor authentication** or transaction
confirmation: the password is valid **only once** and is
often time-limited (e.g., 30–60 seconds).

## HOTP and TOTP: what is the difference and when to choose which one?

### HOTP

**Characteristics:**

* Code generation is based on a **counter** rather than time.
* A code is generated **only upon an explicit event** (e.g., pressing a button on a hardware token).
* The server and client must maintain counter synchronization.
* A code remains valid **until it is used**, without time-based expiration.

**Use cases:**

| Scenario                              | Example                                  |
| ------------------------------------- | ---------------------------------------- |
| Hardware tokens                       | USB token, banking key fob with a button |
| Systems without reliable time sources | Devices lacking accurate clocks          |
| Small-scale systems with manual entry | Internal corporate applications          |

**Advantages:**

* Suitable for offline hardware tokens.
* Codes do not expire until consumed.

**Limitations:**

* Requires counter synchronization.
* If multiple codes are skipped, the server must implement a “look-ahead window.”

---

### TOTP

**Characteristics:**

* Code generation is based on **time** (typically 30-second intervals).
* The server and client must maintain reasonably synchronized clocks.
* Each code is valid only for a short duration (commonly 30–60 seconds).

**Use cases:**

| Scenario                        | Example                                       |
| ------------------------------- | --------------------------------------------- |
| Two-factor authentication (2FA) | Google Authenticator, Microsoft Authenticator |
| Mobile applications             | Token embedded in a smartphone                |
| High-security web services      | GitHub, AWS, online banking applications      |

**Advantages:**

* Codes are automatically refreshed at regular intervals.
* Does not require counter synchronization, only clock alignment.
* Widely adopted and familiar to users.

**Limitations:**

* Relies on accurate device time.
* Significant clock drift renders codes invalid.

---

## Practical Guidance

* **HOTP** → Recommended when using hardware tokens or in environments without reliable time synchronization.
* **TOTP** → Recommended when accurate time is available and time-based code rotation is expected (e.g., mobile or web-based authentication).
