#!/usr/bin/env python3
"""
Полный парсер расходников для Ambershire (Turtle WoW)
Собирает ВСЕ предметы из профессий: Alchemy, Cooking, Enchanting, Engineering, First Aid
"""

import json
import time
import re
from typing import Dict, List, Set, Optional
import requests
from bs4 import BeautifulSoup


# Профессии для парсинга
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
    """
    Парсит страницу профессии и извлекает все itemID
    """
    url = PROFESSION_BASE_URL.format(profession=profession)
    print(f"\nFetching {profession} page...", end=" ")
    
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Ищем все ссылки на предметы
        item_links = soup.find_all('a', href=re.compile(r'/auctionHouse/turtle-wow/ambershire/mergedAh/[^/]+-(\d+)$'))
        
        item_ids = set()
        for link in item_links:
            href = link.get('href')
            match = re.search(r'-(\d+)$', href)
            if match:
                item_id = int(match.group(1))
                item_ids.add(item_id)
        
        print(f"OK (found {len(item_ids)} items)")
        return item_ids
        
    except Exception as e:
        print(f"ERROR: {e}")
        return set()


def fetch_item_price(item_id: int, days: int = 7) -> Optional[int]:
    """
    Получает среднюю цену предмета за последние N дней
    """
    url = API_BASE.format(itemid=item_id)
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if not data:
            return None
        
        # Берём последние N дней
        recent_entries = list(data.items())[-days * 24:]
        
        if not recent_entries:
            return None
        
        # Считаем среднюю цену
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
    print("Full Ambershire Consumables Scraper for Turtle WoW")
    print("=" * 70)
    
    # Шаг 1: Собираем все itemID из профессий
    print("\n[STEP 1] Collecting item IDs from professions...")
    all_items = set()
    
    for profession in PROFESSIONS:
        items = fetch_profession_items(profession)
        all_items.update(items)
        time.sleep(1)  # Rate limiting
    
    print(f"\nTotal unique items found: {len(all_items)}")
    
    if not all_items:
        print("ERROR: No items found! Check if site structure changed.")
        return
    
    # Шаг 2: Собираем цены
    print("\n[STEP 2] Fetching prices...")
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
        
        # Rate limiting
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
    
    output_file = "ambershire-prices-full.json"
    with open(output_file, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nSaved to: {output_file}")
    
    # Статистика
    if prices:
        avg_price = sum(prices.values()) / len(prices)
        min_price = min(prices.values())
        max_price = max(prices.values())
        
        print("\n" + "=" * 70)
        print("Price Statistics:")
        print(f"  Average: {avg_price:.0f} copper ({avg_price/10000:.2f}g)")
        print(f"  Min: {min_price} copper ({min_price/10000:.2f}g)")
        print(f"  Max: {max_price} copper ({max_price/10000:.2f}g)")
    
    if failed:
        print(f"\nFailed items (saved to failed-items.txt): {len(failed)}")
        with open("failed-items.txt", "w") as f:
            for item_id in sorted(failed):
                f.write(f"{item_id}\n")
    
    print("\nDone!")


if __name__ == "__main__":
    main()