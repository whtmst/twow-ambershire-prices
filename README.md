# Turtle WoW Ambershire Prices Database

Automated price tracking system for consumables and trade goods on Turtle WoW Ambershire server.

## 📊 Live Prices

**Main File (Recommended):** [`ambershire-prices-filtered.json`](https://raw.githubusercontent.com/whtmst/twow-ambershire-prices/main/ambershire-prices-filtered.json)  
*155 essential consumables for summarize_consumes tool*

**Full Database:** [`ambershire-prices-full.json`](https://raw.githubusercontent.com/whtmst/twow-ambershire-prices/main/ambershire-prices-full.json)  
*453 items from all professions*

**Last updated:** ![Last Updated](https://img.shields.io/github/last-commit/whtmst/twow-ambershire-prices/main?label=last%20update)

## 🚀 Features

- **🔄 Fully Automated** - Weekly price updates via GitHub Actions
- **🎯 Two Versions** - Filtered (155 items) and Full (453 items)
- **💰 Real-time Data** - Average prices from last 7 days of auction house data
- **🔧 Easy Integration** - Simple JSON API for developers
- **📊 Statistics** - Price trends and market analysis

## 📁 File Versions

### 🎯 Filtered Version (`ambershire-prices-filtered.json`)
- **155 items** - Only consumables defined in [`consumable_db.py`](https://github.com/melbaa/summarize_consumes/blob/master/src/melbalabs/summarize_consumes/consumable_db.py)
- **89% success rate** - 138/155 items with auction data
- **Perfect for** - [`summarize_consumes`](https://github.com/melbaa/summarize_consumes) tool
- **Optimized** - No unnecessary items, faster processing

### 📦 Full Version (`ambershire-prices-full.json`)
- **453 items** - All items from Alchemy, Cooking, Enchanting, Engineering, First Aid
- **85% success rate** - 384/453 items with auction data
- **Perfect for** - General market analysis, profession calculators
- **Comprehensive** - Includes all trade goods and materials

## 🛠 Usage

### For summarize_consumes Tool

Update your `main.py` to use Ambershire prices:

```python
URLS = {
    "nord": "https://melbalabs.com/static/twowprices.json",
    "telabim": "https://melbalabs.com/static/twowprices-telabim.json", 
    "ambershire": "https://raw.githubusercontent.com/whtmst/twow-ambershire-prices/main/ambershire-prices-filtered.json",
}
```

Then run:
```bash
python -m src.melbalabs.summarize_consumes.main "path/to/log.txt" --prices-server ambershire
```

### For Developers

Use our JSON API in your applications:

```python
import requests

# Fetch filtered prices (recommended)
url = "https://raw.githubusercontent.com/whtmst/twow-ambershire-prices/main/ambershire-prices-filtered.json"
response = requests.get(url)
prices_data = response.json()

# Or fetch full database
url_full = "https://raw.githubusercontent.com/whtmst/twow-ambershire-prices/main/ambershire-prices-full.json"

# Access prices
last_update = prices_data["last_update"]  # Unix timestamp
prices = prices_data["data"]              # {item_id: price_in_copper}

# Example: Get price for item ID 13452 (Elixir of the Mongoose)
item_price = prices.get("13452")
if item_price:
    gold = item_price / 10000
    print(f"Price: {gold:.2f}g")
```

## 📈 Coverage

### Filtered Version (155 items)
- **All consumables** from original `consumable_db.py`
- **Mana Potions, Healing Potions, Elixirs, Flasks, Oils, Jujus**
- **Success Rate**: 89% (138/155 items with prices)

### Full Version (453 items)
- **Alchemy**: 117 items
- **Cooking**: 89 items  
- **Enchanting**: 16 items
- **Engineering**: 160 items
- **First Aid**: 14 items
- **Success Rate**: 85% (384/453 items with prices)

## 🔧 Technical Details

### Data Sources
- **Auction Data**: [WowAuctions.net](https://www.wowauctions.net) API
- **Item Database**: Turtle WoW profession pages + consumable_db.py
- **Update Frequency**: Weekly (every Monday 00:00 UTC)

### Price Calculation
- Uses 7-day moving average
- Filters outliers and invalid data  
- Prices in copper (1g = 10,000 copper)

### File Format
```json
{
  "last_update": 1739132805,
  "total_items": 155,
  "successful_items": 138,
  "failed_items": 17,
  "data": {
    "item_id": price_in_copper,
    "13452": 3851,
    "13453": 7878,
    ...
  }
}
```

## 🤝 Contributing

### Report Issues
- Missing consumables in filtered version
- Incorrect prices
- API changes

### Manual Update
```bash
# Run filtered parser (recommended)
python filtered_scraper.py

# Run full parser
python full_scraper.py
```

## 📊 Statistics

**Filtered Version:**  
![Filtered Success](https://img.shields.io/badge/filtered_success-89%25-brightgreen) ![Filtered Items](https://img.shields.io/badge/items-155-blue)

**Full Version:**  
![Full Success](https://img.shields.io/badge/full_success-85%25-green) ![Full Items](https://img.shields.io/badge/items-453-orange)

**Price Range:**  
![Average Price](https://img.shields.io/badge/average_price-3.61g-green) ![Min Price](https://img.shields.io/badge/min_price-0.00g-lightgrey) ![Max Price](https://img.shields.io/badge/max_price-552.83g-red)

## 🔗 Related Projects

- [summarize_consumes](https://github.com/melbaa/summarize_consumes) - Raid consumables analysis tool
- [WowAuctions.net](https://www.wowauctions.net) - Turtle WoW auction data

## 📄 License

MIT License - feel free to use this data in your projects!

---

**Maintained by**: [whtmst](https://github.com/whtmst)

*This project is not affiliated with Turtle WoW or Blizzard Entertainment.*
