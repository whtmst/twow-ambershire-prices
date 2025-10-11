#!/usr/bin/env python3
"""
Фильтрованный парсер для Ambershire - только нужные consumables из consumable_db.py
"""

import json
import time
import re
from typing import Dict, List, Set, Optional
import requests
from bs4 import BeautifulSoup

# Список ВСЕХ нужных itemid из consumable_db.py
NEEDED_ITEMIDS = {
    # Базовые компоненты
    8831,   # Purple Lotus
    14344,  # Large Brilliant Shard
    8393,   # Scorpok Pincer
    8392,   # Blasted Boar Lung
    8391,   # Snickerfang Jowl
    8394,   # Basilisk Brain
    8396,   # Vulture Gizzard
    19698,  # Zulian Coin
    8150,   # Deeprock Salt
    7078,   # Essence of Fire
    18512,  # Larval Acid
    61198,  # Small Dream Shard
    61199,  # Bright Dream Shard
    11185,  # Green Power Crystal
    11184,  # Blue Power Crystal
    11186,  # Red Power Crystal
    11188,  # Yellow Power Crystal
    
    # Consumables
    20748,  # Brilliant Mana Oil
    20747,  # Lesser Mana Oil
    23123,  # Blessed Wizard Oil
    20749,  # Brilliant Wizard Oil
    20750,  # Wizard Oil
    3829,   # Frost Oil
    3824,   # Shadow Oil
    13447,  # Elixir of the Sages
    9187,   # Elixir of Greater Agility
    13445,  # Elixir of Superior Defense
    5634,   # Free Action Potion
    17708,  # Elixir of Frost Power
    13454,  # Greater Arcane Elixir
    7676,   # Thistle Tea
    13453,  # Elixir of Brute Force
    12820,  # Winterfall Firewater
    5633,   # Great Rage Potion
    5631,   # Rage Potion
    12431,  # Juju Power
    12430,  # Juju Flurry
    12436,  # Juju Might
    12433,  # Juju Guile
    12435,  # Juju Escape
    12432,  # Juju Ember
    12434,  # Juju Chill
    53015,  # Gurubashi Gumbo
    51717,  # Hardened Mushroom
    8956,   # Oil of Immolation
    4623,   # Lesser Stoneshield Potion
    13455,  # Greater Stoneshield
    61225,  # Lucidity Potion
    3827,   # Mana Potion
    6149,   # Mana Potion - Greater
    13443,  # Mana Potion - Superior
    13444,  # Mana Potion - Major
    13446,  # Healing Potion - Major
    3928,   # Healing Potion - Superior
    9206,   # Elixir of Giants
    21151,  # Rumsey Rum Black Label
    21114,  # Rumsey Rum Dark
    18262,  # Elemental Sharpening Stone
    23122,  # Consecrated Sharpening Stone
    3387,   # Invulnerability
    12217,  # Dragonbreath Chili
    61423,  # Dreamtonic
    10646,  # Goblin Sapper Charge
    61175,  # Medivh's Merlot Blue Label
    61174,  # Medivh's Merlot
    13461,  # Greater Arcane Protection Potion
    13460,  # Greater Holy Protection Potion
    13459,  # Greater Shadow Protection Potion
    13458,  # Greater Nature Protection Potion
    13457,  # Greater Fire Protection Potion
    13456,  # Greater Frost Protection Potion
    6051,   # Holy Protection Potion
    6048,   # Shadow Protection Potion
    6052,   # Nature Protection Potion
    6049,   # Fire Protection Potion
    6050,   # Frost Protection Potion
    61224,  # Dreamshard Elixir
    18641,  # Dense Dynamite
    10507,  # Solid Dynamite
    9088,   # Gift of Arthas
    15993,  # Thorium Grenade
    4390,   # Iron Grenade
    13928,  # Grilled Squid
    9179,   # Elixir of Greater Intellect
    18253,  # Rejuvenation Potion - Major
    2456,   # Rejuvenation Potion - Minor
    2459,   # Swiftness Potion
    9172,   # Invisibility Potion
    3823,   # Lesser Invisibility Potion
    19440,  # Powerful Anti-Venom
    6453,   # Strong Anti-Venom
    6452,   # Anti-Venom
    54010,  # Dissolvent Poison II
    20520,  # Dark Rune
    20007,  # Mageblood Potion
    60976,  # Danonzo's Tel'Abim Surprise
    60977,  # Danonzo's Tel'Abim Delight
    60978,  # Danonzo's Tel'Abim Medley
    9144,   # Wildvine Potion
    10307,  # Scroll of Stamina IV
    10310,  # Scroll of Strength IV
    10306,  # Scroll of Spirit IV
    10305,  # Scroll of Protection IV
    10308,  # Scroll of Intellect IV
    10309,  # Scroll of Agility IV
    13462,  # Purification Potion
    5823,   # Poisonous Mushroom
    13931,  # Nightfin Soup
    3382,   # Weak Troll's Blood Potion
    3388,   # Strong Troll's Blood Potion
    20004,  # Major Troll's Blood Potion
    3826,   # Mighty Troll's Blood Potion
    9036,   # Magic Resistance Potion
    2633,   # Jungle Remedy
    20008,  # Living Action Potion
    83309,  # Empowering Herbal Salad
    3386,   # Elixir of Poison Resistance
    9224,   # Elixir of Demonslaying
    17407,  # Graccu's Homemade Meat Pie
    20002,  # Greater Dreamless Sleep Potion
    8951,   # Elixir of Greater Defense
    6662,   # Elixir of Giant Growth
    22682,  # Frozen Rune
    9155,   # Arcane Elixir
    12404,  # Dense Sharpening Stone
    12643,  # Dense Weightstone
    6373,   # Elixir of Firepower
    21546,  # Elixir of Greater Firepower
    9264,   # Elixir of Shadow Power
    61181,  # Potion of Quickness
    84040,  # Le Fishe Au Chocolat
    13452,  # Elixir of the Mongoose
    50237,  # Elixir of Greater Nature Power
    51720,  # Power Mushroom
    13442,  # Mighty Rage Potion
    13935,  # Baked Salmon
    84041,  # Gilneas Hot Stew
    51718,  # Juicy Striped Melon
    2091,   # Magic Dust
    12190,  # Dreamless Sleep Potion
    47410,  # Concoction of the Emerald Mongoose
    47412,  # Concoction of the Arcane Giant
    47414,  # Concoction of the Dreamwater
    
    # Добавляем недостающие из твоего текущего файла которые могут быть нужны
    3825,   # Elixir of Fortitude
    13510,  # Flask of the Titans
    13512,  # Flask of Supreme Power
    13511,  # Flask of Distilled Wisdom
    13513,  # Flask of Chromatic Resistance
    19183,  # Hourglass Sand
    4392,   # Advanced Target Dummy
    16023,  # Masterwork Target Dummy
}

# Остальной код твоего парсера остается таким же...
PROFESSIONS = [
    "alchemy",
    "cooking", 
    "enchanting",
    "engineering",
    "first-aid",
]

PROFESSION_BASE_URL = "https://www.wowauctions.net/professions/turtle-wow/ambershire/mergedAh/{profession}"
API_BASE = "https://api.wowauctions.net/items/stats/30d/ambershire/mergedAh/{itemid}"


def fetch_profession_items(profession: str) -> Set[int]:
    """Парсит страницу профессии и извлекает все itemID"""
    url = PROFESSION_BASE_URL.format(profession=profession)
    print(f"\nFetching {profession} page...", end=" ")
    
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        item_links = soup.find_all('a', href=re.compile(r'/auctionHouse/turtle-wow/ambershire/mergedAh/[^/]+-(\d+)$'))
        
        item_ids = set()
        for link in item_links:
            href = link.get('href')
            match = re.search(r'-(\d+)$', href)
            if match:
                item_id = int(match.group(1))
                # ФИЛЬТРУЕМ: оставляем только нужные itemid
                if item_id in NEEDED_ITEMIDS:
                    item_ids.add(item_id)
        
        print(f"OK (found {len(item_ids)} needed items)")
        return item_ids
        
    except Exception as e:
        print(f"ERROR: {e}")
        return set()


def fetch_item_price(item_id: int, days: int = 7) -> Optional[int]:
    """Получает среднюю цену предмета за последние N дней"""
    url = API_BASE.format(itemid=item_id)
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if not data:
            return None
        
        recent_entries = list(data.items())[-days * 24:]
        if not recent_entries:
            return None
        
        prices = []
        for timestamp, stats in recent_entries:
            avg_price = stats.get("avg_price")
            if avg_price and avg_price > 0:
                prices.append(avg_price)
        
        if not prices:
            return None
        
        return int(sum(prices) / len(prices))
        
    except Exception:
        return None


def main():
    print("=" * 70)
    print("FILTERED Ambershire Consumables Scraper for Turtle WoW")
    print(f"Target items: {len(NEEDED_ITEMIDS)}")
    print("=" * 70)
    
    # Шаг 1: Собираем только нужные itemID
    print("\n[STEP 1] Collecting filtered item IDs from professions...")
    all_items = set()
    
    for profession in PROFESSIONS:
        items = fetch_profession_items(profession)
        all_items.update(items)
        time.sleep(1)
    
    print(f"\nTotal needed items found: {len(all_items)}")
    
    # Шаг 2: Собираем цены
    print("\n[STEP 2] Fetching prices for needed items...")
    print("-" * 70)
    
    prices = {}
    failed = []
    
    for idx, item_id in enumerate(sorted(all_items), 1):
        print(f"[{idx}/{len(all_items)}] Item {item_id}...", end=" ")
        
        price = fetch_item_price(item_id, days=7)
        
        if price is not None:
            prices[str(item_id)] = price
            print(f"OK ({price} copper = {price/10000:.2f}g)")
        else:
            failed.append(item_id)
            print("NO DATA")
        
        time.sleep(0.3)
    
    print()
    print("=" * 70)
    print(f"Successfully fetched: {len(prices)}/{len(all_items)}")
    print(f"Failed (no auction data): {len(failed)}")
    
    # Шаг 3: Сохраняем результат
    output = {
        "last_update": int(time.time()),
        "data": prices
    }
    
    output_file = "ambershire-prices-filtered.json"
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nSaved to: {output_file}")
    
    # Показываем какие предметы не найдены
    missing_items = NEEDED_ITEMIDS - all_items
    if missing_items:
        print(f"\nMissing items (not found in professions): {len(missing_items)}")
        with open("missing-items.txt", "w") as f:
            for item_id in sorted(missing_items):
                f.write(f"{item_id}\n")
    
    print("\nDone!")


if __name__ == "__main__":
    main()
