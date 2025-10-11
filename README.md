# Turtle WoW Ambershire Prices Database

Automated price tracking system for consumables and trade goods on Turtle WoW Ambershire server.

## 📊 Live Prices

**Current prices file:** [`ambershire-prices-full.json`](https://raw.githubusercontent.com/whtmst/twow-ambershire-prices/main/ambershire-prices-full.json)

**Last updated:** ![Last Updated](https://img.shields.io/github/last-commit/whtmst/twow-ambershire-prices/main?label=last%20update)

## 🚀 Features

- **🔄 Fully Automated** - Weekly price updates via GitHub Actions
- **📈 396+ Items** - Covers all professions: Alchemy, Cooking, Enchanting, Engineering, First Aid
- **💰 Real-time Data** - Average prices from last 7 days of auction house data
- **🔧 Easy Integration** - Simple JSON API for developers
- **📊 Statistics** - Price trends and market analysis

## 🛠 Usage

### For Developers

Use our JSON API in your applications:

```python
import requests

# Fetch latest prices
url = "https://raw.githubusercontent.com/whtmst/twow-ambershire-prices/main/ambershire-prices-full.json"
response = requests.get(url)
prices_data = response.json()

# Access prices
last_update = prices_data["last_update"]  # Unix timestamp
prices = prices_data["data"]              # {item_id: price_in_copper}

# Example: Get price for item ID 13452 (Stonescale Eel)
item_price = prices.get("13452")
if item_price:
    gold = item_price / 10000
    print(f"Price: {gold:.2f}g")
```

### With summarize_consumes Tool

Update your `main.py` to use:

```python
URLS = {
  "nord": "https://melbalabs.com/static/twowprices.json",
  "telabim": "https://melbalabs.com/static/twowprices-telabim.json",
  "ambershire": "https://gist.githubusercontent.com/whtmst/7d240b57d8f85029d33629ad4a86a2dd/raw/c5e11696815f2eea7e67416ed818b1f1231a95eb/ambershire-prices.json",
  }
```
```python
parser.add_argument(
  "--prices-server",
  choices=["nord", "telabim", "ambershire"],
  default="nord",
  help="specify which server price data to use",
  )
```

Then run:
```bash
python -m src.melbalabs.summarize_consumes.main "path/to/log.txt" --prices-server ambershire
```

## 📈 Coverage

- **Alchemy**: 117 items
- **Cooking**: 89 items  
- **Enchanting**: 16 items
- **Engineering**: 160 items
- **First Aid**: 14 items

**Total tracked items**: 396
**Success rate**: ~84% (332/396 items with auction data)

## 🔧 Technical Details

### Data Sources
- **Auction Data**: [WowAuctions.net](https://www.wowauctions.net) API
- **Item Database**: Turtle WoW profession pages
- **Update Frequency**: Weekly (every Monday 00:00 UTC)

### Price Calculation
- Uses 7-day moving average
- Filters outliers and invalid data
- Prices in copper (1g = 10,000 copper)

### File Format
```json
{
  "last_update": 1739132805,
  "data": {
    "item_id": price_in_copper,
    "13452": 3851,
    "13453": 7878,
    ...
  }
}
```

## 🤝 Contributing

### Manual Update
```bash
python ambershire_full_scraper.py
```

### Report Issues
- Missing items
- Incorrect prices
- API changes

## 📊 Statistics

![Average Price](https://img.shields.io/badge/average_price-4.12g-green)
![Min Price](https://img.shields.io/badge/min_price-0.00g-lightgrey)
![Max Price](https://img.shields.io/badge/max_price-556.17g-red)

## 🔗 Related Projects

- [summarize_consumes](https://github.com/melbaa/summarize_consumes) - Raid consumables analysis tool
- [WowAuctions.net](https://www.wowauctions.net) - Turtle WoW auction data

## 📄 License

MIT License - feel free to use this data in your projects!

---

**Maintained by**: [whtmst](https://github.com/whtmst)

*This project is not affiliated with Turtle WoW or Blizzard Entertainment.*
