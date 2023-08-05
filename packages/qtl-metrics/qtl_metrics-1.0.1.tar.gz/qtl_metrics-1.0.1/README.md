# Quantalon Metrics

## QuickStart

```
import yfinance as yf
from qtl_metrics import Metrics

aapl = yf.Ticker("AAPL")
data = aapl.history()
prices = data['Close']
metrics = Metrics(prices)

print(metrics.stats)
```