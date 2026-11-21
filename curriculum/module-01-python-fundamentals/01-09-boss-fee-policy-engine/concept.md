## Boss Fight: Multi-File Fee & Policy Evaluator Engine

Your payment platform processes merchant payouts under strict tier policies and compliance gates. A naive prototype used floating-point arithmetic, swallowed invalid rule shapes, and lacked deterministic summary formatting.

### Architecture (`models.py` + `engine.py`)
* `models.py` defines the domain exception `PolicyEvaluationError` and policy rate lookup helpers.
* `engine.py` evaluates transaction requests, enforces compliance checks, computes exact `Decimal` fees (`ROUND_HALF_UP`), and formats an audit summary line.

### Rules & Contract
1. **Policy Routing (`models.py` -> `resolve_fee_rate(policy)`):**
   * `{"tier": "enterprise", "monthly_volume": int(v)}` with `v >= 100_000` -> `Decimal("0.0125")`
   * `{"tier": "enterprise"}` -> `Decimal("0.0175")`
   * `{"tier": "growth", "high_risk": True}` -> `Decimal("0.0350")`
   * `{"tier": "growth"}` -> `Decimal("0.0250")`
   * `{"tier": "starter"}` -> `Decimal("0.0290")`
   * Any other policy shape raises `PolicyEvaluationError`.
2. **Fee Evaluation (`engine.py` -> `evaluate_payout(...)`):**
   * Convert `amount_str` to `Decimal` (wrap `InvalidOperation` with `raise PolicyEvaluationError(...) from exc`; reject `<= 0`).
   * Enforce `checks` (non-empty list of booleans—all must be `True`, else raise `PolicyEvaluationError("Compliance gate failed")`).
   * Compute `fee = (amount * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)` and `net = amount - fee`, with optional keyword-only `*, override_rate: Decimal | None = None`.
   * Return `{"merchant": merchant.strip(), "gross": amount, "fee": fee, "net": net, "rate": rate}`.
3. **Summary Formatting (`engine.py` -> `format_payout_summary(result)`):**
   * Return `f"{merchant:<14} | gross={gross:>9.2f} | fee={fee:>7.2f} | net={net:>9.2f}"`.
