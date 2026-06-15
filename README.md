# ⚡ KMA Fleet Ledger & Performance Metrics

> **Architecture:** Automated Vision-Sync Bot -> Local Database -> GitHub Pipeline -> Stellar Soroban Immutable Vault

## 📊 Master Performance Metrics

| Metric Component | Current Value | Benchmark Comparison |
| :--- | :--- | :--- |
| **Total Deposited Capital** | $14.00 USD | (Initial $3.00 + Recent $11.00) |
| **Total Withdrawn Capital** | $55.00 USD | 🟢 Risk-Free / House Money Secured |
| **Total Account Equity** | $138.36 USD | Live Liquidation Value |
| **Net Value Generated** | $193.36 USD | (Equity + Withdrawals) |
| **Net Return (%)** | +1,281.14% | Tracked vs Initial Deposits |
| **Unrealized PNL (Floating)** | +$125.92 USD | Active Runners (BTC, HYPE) |

---

## 🗃️ Chronological Transaction Ledger

| ID | Timestamp (UTC) | Asset | Type | Entry | Size | Leverage | Exit | Net PNL (USD) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `000` | 2026-06-12 08:00 | USDT | DEPOSIT | N/A | N/A | N/A | N/A | $3.00 | COMPLETE |
| `001` | 2026-06-14 21:00 | USDT | DEPOSIT | N/A | N/A | N/A | N/A | $11.00 | COMPLETE |
| `006` | 2026-06-15 09:00 | BTC | LONG | 63,821.0 | 0.0698 | 500x | RUNNING | +$132.74 | 🟢 RUNNING |
| `007` | 2026-06-15 09:00 | HYPE | LONG | 60.643 | 5.6 | 100x | RUNNING | +$24.61 | 🟢 RUNNING |
| `008` | 2026-06-15 10:04 | ETH | CLOSE | 1,715.12 | 6.64 | 500x | 1,718.91 | +$24.47 | COMPLETE |
| `009` | 2026-06-15 10:19 | BTC | PARTIAL | 63,821.0 | 0.0160 | 500x | 65,634.6 | +$29.01 | COMPLETE |
| `010` | 2026-06-15 10:20 | USDT | WITHDRAW | N/A | N/A | N/A | N/A | -$55.00 | COMPLETE |

---
*System synchronized natively via MacBook Air background daemon.*