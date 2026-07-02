# Django Unchained: The Frontier Bounty Board 🎯

Welcome to the digital ledger of the Wild West. This repository hosts a secure, robust REST API built with Django and Django REST Framework (DRF) to track outlaws, rewards, and captures across the frontier. 

To protect the town's records from outlaws, cheats, and malicious agents, the system is reinforced with object-level security, payload validation, strict rate limiting, and invalidation-aware caching.

---

## 🤠 Frontier Concept Selection

* **Concept Picked:** 🎯 **Bounty Board**
* **Data Mapping:**
    * `target_name`: The name of the outlaw wanted by the law.
    * `reward`: The bounty amount (in dollars) placed on their head.
    * `status`: The operational state of the contract (`wanted` or `captured`).
    * `owner`: The specific lawman/sheriff who posted and manages the bounty.

---

## 🛡️ Defensive Architecture (Security & Grader Specs)

Our frontier outpost is defended against four primary threat categories:

### 1. Access Control & Information Leak Prevention
* **Isolation by Scope:** We explicitly override `get_queryset()` in both the list and detail views to filter records strictly by `request.user`. 
* **Anti-Snooping (No 403 Leaks):** If an attacker tries to guess or sequentially increment a bounty ID belonging to another user (e.g., `/api/bounties/99/`), the server returns a clean `404 Not Found` instead of a `403 Forbidden`. This hides whether the record even exists, preventing information mapping.

### 2. Malformed & Hostile Input Validation
* **Sanitizing Payloads:** The `BountySerializer` enforces data integrity. The `reward` field is validated to ensure it is never negative, and `status` strictly rejects values outside of `wanted` or `captured`.
* **Implicit Identity Mapping:** The `owner` field is marked as a `ReadOnlyField`. It cannot be overridden via a malicious JSON payload; it is always injected securely from the validated JWT token session.

### 3. [Bonus] Request Burst Protection (Rate Limiting)
* **Anonymous Throttle (`AnonRateThrottle`):** Registration and login endpoints are throttled to **20 requests/minute** to eliminate automated brute-force attacks and registry spam.
* **Authenticated Throttle (`UserRateThrottle`):** Logged-in users are rate-limited to **100 requests/minute** across data views to maintain server stability during massive request bursts.

### 4. [Bonus] High-Performance Caching with Fresh Invalidation
* **Per-User Isolation:** Read-heavy GET operations on the bounty list are cached in-memory unique to each user's ID (`bounties_list_<user_id>`).
* **Data Freshness Enforcement:** To avoid serving stale data, the cache is explicitly invalidated (`cache.delete()`) the exact moment a user performs a write operation (`POST`, `PUT`, `PATCH`, or `DELETE`). 

---

## 🚀 Quickstart & Installation

This project relies on zero external container services or background databases. It runs out of the box using standard Python and a local SQLite footprint.

### 1. Setup Environment
```bash
# Clone the repository and navigate inside
cd your-rollno-django-unchained/

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install non-negotiable and supporting dependencies
pip install -r requirements.txt# 25B0347_DjangoUnchained
