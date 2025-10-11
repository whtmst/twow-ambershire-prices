#!/usr/bin/env python3
"""
Фильтрованный парсер для Ambershire - сканирует ВСЕ нужные consumables из consumable_db.py напрямую через API
"""

import json
import time
from typing import Dict, List, Optional
import requests

# Список ВСЕХ нужных itemid из consumable_db.py (154 предмета)
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
    
    # Дополнительные важные предметы
    3825,   # Elixir of Fortitude
    13510,  # Flask of the Titans
    13512,  # Flask of Supreme Power
    13511,  # Flask of Distilled Wisdom
    13513,  # Flask of Chromatic Resistance
    19183,  # Hourglass Sand
    4392,   # Advanced Target Dummy
    16023,  # Masterwork Target Dummy
    5206,   # Bogling Root
    1703,   # Crystal Basilisk Spine
    9030,   # Restorative Potion
    13506,  # Flask of Petrification
    53015,  # Gurubashi Gumbo
    61225,  # Lucidity Potion
    61181,  # Potion of Quickness
    84040,  # Le Fishe Au Chocolat
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
}

API_BASE = "https://api.wowauctions.net/items/stats/30d/ambershire/mergedAh/{itemid}"


def fetch_item_price(item_id: int, days: int = 7) -> Optional[int]:
    """Получает среднюю цену предмета за последние N дней"""
    url = API_BASE.format(itemid=item_id)
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if not data:
            return None
        
        # Берем данные за последние N дней
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
        
    except Exception as e:
        print(f"ERROR for item {item_id}: {e}")
        return None


def main():
    print("=" * 70)
    print("ENHANCED FILTERED Ambershire Consumables Scraper for Turtle WoW")
    print(f"Total target items: {len(NEEDED_ITEMIDS)}")
    print("=" * 70)
    
    # Прямой запрос цен для ВСЕХ нужных itemid
    print("\n[STEP 1] Direct price fetching for ALL needed items...")
    print("-" * 70)
    
    prices = {}
    failed = []
    successful = 0
    
    for idx, item_id in enumerate(sorted(NEEDED_ITEMIDS), 1):
        print(f"[{idx}/{len(NEEDED_ITEMIDS)}] Item {item_id}...", end=" ")
        
        price = fetch_item_price(item_id, days=7)
        
        if price is not None:
            prices[str(item_id)] = price
            successful += 1
            print(f"OK ({price} copper = {price/10000:.2f}g)")
        else:
            failed.append(item_id)
            print("NO DATA")
        
        # Задержка чтобы не заDDOSить API
        time.sleep(0.3)
    
    print()
    print("=" * 70)
    print(f"SUCCESSFULLY fetched: {successful}/{len(NEEDED_ITEMIDS)} items")
    print(f"FAILED (no auction data): {len(failed)} items")
    
    if failed:
        print(f"\nFailed items: {sorted(failed)}")
        
        # Сохраняем список неудачных предметов
        with open("failed-items.txt", "w") as f:
            for item_id in sorted(failed):
                f.write(f"{item_id}\n")
    
    # Сохраняем результат
    output = {
        "last_update": int(time.time()),
        "total_items": len(NEEDED_ITEMIDS),
        "successful_items": successful,
        "failed_items": len(failed),
        "data": prices
    }
    
    output_file = "ambershire-prices-filtered.json"
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nSaved to: {output_file}")
    print(f"File contains {len(prices)} items with prices")
    
    # Статистика
    print("\n" + "=" * 70)
    print("SUMMARY:")
    print(f"  Total items in filter: {len(NEEDED_ITEMIDS)}")
    print(f"  Items with prices: {successful}")
    print(f"  Items without data: {len(failed)}")
    print(f"  Success rate: {(successful/len(NEEDED_ITEMIDS))*100:.1f}%")
    
    print("\nDone!")


if __name__ == "__main__":
    main()
