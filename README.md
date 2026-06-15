# ⚡ KMA Fleet Ledger & Performance Metrics

> **Architecture:** Automated Vision-Sync Bot -> Local Database -> GitHub Pipeline -> Stellar Soroban Immutable Vault

## 📊 Master Performance Metrics

| Metric Component | Current Value | Benchmark Comparison |
| :--- | :--- | :--- |
| **Total Deposited Capital** | $14.00 USD | (Initial $3.00 + Recent $11.00) |
| **Total Withdrawn Capital** | $94.61 USD | 🟢 Swept to Spot Vault |
| **Active Futures Equity** | $101.76 USD | 🛡️ Operational Baseline Maintained |
| **Net Value Generated** | $196.37 USD | (Equity + Withdrawals) |
| **Net Return (%)** | +1,302.64% | Tracked vs Initial Deposits |
| **Active Risk Status** | ZERO RISK | Hard SL at 63,919.1. BTC Leverage dialed down to 100x. |

---

## 🗃️ Chronological Transaction Ledger

| ID | Timestamp (UTC) | Asset | Type | Entry | Exit | Net PNL (USD) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `000` | 2026-06-12 08:00 | USDT | DEPOSIT | N/A | N/A | $3.00 | COMPLETE |
| `001` | 2026-06-14 21:00 | USDT | DEPOSIT | N/A | N/A | $11.00 | COMPLETE |
| `006` | 2026-06-15 09:00 | BTC | LONG | 63,821.0 | RUNNING | +$76.84 | 🛡️ SECURED (100x) |
| `009` | 2026-06-15 10:19 | BTC | PARTIAL | 63,821.0 | 65,634.6 | +$29.01 | COMPLETE |
| `010` | 2026-06-15 10:20 | USDT | WITHDRAW | N/A | N/A | -$55.00 | COMPLETE |
| `011` | 2026-06-15 12:00 | HYPE | PARTIAL | 60.643 | 66.655 | +$6.61 | COMPLETE |
| `012` | 2026-06-15 12:25 | HYPE | PARTIAL | 60.643 | 67.191 | +$5.89 | COMPLETE |
| `013` | 2026-06-15 12:25 | BTC | PARTIAL | 63,821.0 | 65,702.9 | +$22.20 | COMPLETE |
| `014` | 2026-06-15 12:30 | USDT | WITHDRAW | N/A | N/A | -$39.61 | COMPLETE |
| `015` | 2026-06-15 13:03 | ETH | CLOSE | N/A | 1,733.18 | -$0.95 | COMPLETE |
| `016` | 2026-06-15 13:28 | BTC | PARTIAL | 63,821.0 | 66,230.2 | +$22.16 | COMPLETE |
| `017` | 2026-06-15 13:28 | HYPE | PARTIAL | 60.643 | 67.956 | +$6.58 | COMPLETE |

---
*System synchronized natively via MacBook Air background daemon. Active positions scaled out systematically. Leverage dynamically adjusted down to 100x on BTC to mitigate funding drag.*