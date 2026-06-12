import pandas as pd

def compile_public_dashboard():
    df = pd.read_csv('ledger.csv')
    
    initial_capital = float(df[df['type'] == 'DEPOSIT']['size'].sum())
    net_realized_pnl = float(df['net_pnl_usd'].sum())
    current_balance = initial_capital + net_realized_pnl
    total_return_pct = (net_realized_pnl / initial_capital) * 100
    
    completed_trades = df[df['id'] != '000']
    total_plays = len(completed_trades)
    winning_plays = len(completed_trades[completed_trades['net_pnl_usd'] > 0])
    win_rate = (winning_plays / total_plays * 100) if total_plays > 0 else 0.0

    readme_content = f"""# 📈 The Well & Merchant Trading Journal
### *Our Journey from $3.00 to System Automation*

Welcome to our official public log. This repository serves as our permanent, unedited paper trail. We are tracking our personal evolution from manual operators to automated systems engineers, using the exact 21/200 KMA strategy loops we discuss and refine daily.

## 📊 Master Performance Metrics

| Metric Component | Current Value | Benchmark Comparison |
| :--- | :---: | :--- |
| **Total Account Value** | ${current_balance:.4f} USD | Base Starting Asset: $3.00 |
| **Net Return (%)** | +{total_return_pct:.2f}% | Tracked via live ledger logic |
| **Active Floating Leverage** | 500x Cross | Maximum Risk Limit: 1% per play |
| **Win/Loss Ratio** | {winning_plays} / {total_plays - winning_plays} ({win_rate:.1f}%) | Profit Factor: Multi-stage execution |

## 📑 Chronological Transaction Ledger

| ID | Timestamp (UTC) | Asset | Type | Entry/Size | Leverage | Exit Price | Net PnL ($) | Status |
| :--- | :--- | :--- | :---: | :--- | :---: | :--- | :--- | :--- |
| `000` | 2026-06-12 08:00 | USDT | DEPOSIT | $3.00 | N/A | INIT | $0.00 | COMPLETE |
| `001A` | 2026-06-12 10:19 | ETH | LONG | $1,659.89 | 500x | $1,668.83 | +$0.54 | COMPLETE |
| `001B` | 2026-06-12 15:40 | ETH | LONG | $1,659.89 | 500x | $1,659.69 | -$0.01 | COMPLETE |
"""
    
    with open('README.md', 'w') as f:
        f.write(readme_content)
        
    print(f"📊 Dashboard compiled successfully. Total Return: +{total_return_pct:.2f}% | Wallet: ${current_balance:.4f}")

if __name__ == '__main__':
    compile_public_dashboard()
