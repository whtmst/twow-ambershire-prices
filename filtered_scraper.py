#!/usr/bin/env python3
"""
Скрапер для GitHub Actions с обходом блокировки через прокси
"""

import json
import time
import requests
from typing import Dict, Optional

# Полный список предметов
NEEDED_ITEMIDS = {
    8831, 14344, 8393, 8392, 8391, 8394, 8396, 19698, 8150, 7078, 18512, 61198, 61199,
    11185, 11184, 11186, 11188, 20748, 20747, 23123, 20749, 20750, 3829, 3824, 13447,
    9187, 13445, 5634, 17708, 13454, 7676, 13453, 12820, 5633, 5631, 12431, 12430, 12436,
    12433, 12435, 12432, 12434, 53015, 51717, 8956, 4623, 13455, 61225, 3827, 6149, 13443,
    13444, 13446, 3928, 9206, 21151, 21114, 18262, 23122, 3387, 12217, 61423, 10646, 61175,
    61174, 13461, 13460, 13459, 13458, 13457, 13456, 6051, 6048, 6052, 6049, 6050, 61224,
    18641, 10507, 9088, 15993, 4390, 13928, 9179, 18253, 2456, 2459, 9172, 3823, 19440,
    6453, 6452, 54010, 20520, 20007, 60976, 60977, 60978, 9144, 10307, 10310, 10306, 10305,
    10308, 10309, 13462, 5823, 13931, 3382, 3388, 20004, 3826, 9036, 2633, 20008, 83309,
    3386, 9224, 17407, 20002, 8951, 6662, 22682, 9155, 12404, 12643, 6373, 21546, 9264,
    61181, 84040, 13452, 50237, 51720, 13442, 13935, 84041, 51718, 2091, 12190, 47410,
    47412, 47414, 3825, 13510, 13512, 13511, 13513, 19183, 4392, 16023, 5206, 1703, 9030,
    13506
}

def fetch_with_retry(item_id: int, days: int = 7) -> Optional[int]:
    """Пробуем разные методы с повторными попытками"""
    
    methods = [
        lambda: fetch_direct(item_id),
        lambda: fetch_with_proxy_1(item_id),
        lambda: fetch_with_proxy_2(item_id),
        lambda: fetch_with_proxy_3(item_id),
    ]
    
    for attempt, method in enumerate(methods, 1):
        try:
            print(f"  Attempt {attempt}...", end=" ")
            data = method()
            if data:
                price = process_data(data, days)
                if price:
                    print("SUCCESS")
                    return price
                else:
                    print("NO DATA")
            else:
                print("FAILED")
        except Exception as e:
            print(f"ERROR: {e}")
        
        if attempt < len(methods):
            time.sleep(1)  # Пауза между попытками
    
    return None

def fetch_direct(item_id: int) -> Optional[dict]:
    """Прямой запрос"""
    url = f"https://api.wowauctions.net/items/stats/30d/ambershire/mergedAh/{item_id}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def fetch_with_proxy_1(item_id: int) -> Optional[dict]:
    """Через публичный CORS прокси"""
    url = f"https://api.wowauctions.net/items/stats/30d/ambershire/mergedAh/{item_id}"
    proxy_url = f"https://api.codetabs.com/v1/proxy?quest={url}"
    try:
        response = requests.get(proxy_url, timeout=15)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def fetch_with_proxy_2(item_id: int) -> Optional[dict]:
    """Через другой прокси"""
    url = f"https://api.wowauctions.net/items/stats/30d/ambershire/mergedAh/{item_id}"
    proxy_url = f"https://cors-anywhere.herokuapp.com/{url}"
    try:
        response = requests.get(proxy_url, timeout=15)
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None

def fetch_with_proxy_3(item_id: int) -> Optional[dict]:
    """Через еще один прокси"""
    url = f"https://api.wowauctions.net/items/stats/30d/ambershire/mergedAh/{item_id}"
    proxy_url = f"https://thingproxy.freeboard.io/fetch/{url}"
    try:
        response = requests.get(proxy_url, timeout=15)
        if response.status_code == 200:
            return response.json()
    except:
    return None

def process_data(data: dict, days: int) -> Optional[int]:
    """Обрабатываем данные"""
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

def main():
    print("=" * 70)
    print("GitHub Actions Scraper with Proxy Fallback")
    print(f"Total items: {len(NEEDED_ITEMIDS)}")
    print("=" * 70)
    
    prices = {}
    failed = []
    
    for idx, item_id in enumerate(sorted(NEEDED_ITEMIDS), 1):
        print(f"[{idx}/{len(NEEDED_ITEMIDS)}] Item {item_id}...", end=" ")
        
        price = fetch_with_retry(item_id, days=7)
        
        if price is not None:
            prices[str(item_id)] = price
            print(f"PRICE: {price} copper")
        else:
            failed.append(item_id)
            print("NO DATA")
        
        time.sleep(1.5)  # Увеличиваем задержку
    
    print("\n" + "=" * 70)
    print(f"SUCCESS: {len(prices)} items")
    print(f"FAILED: {len(failed)} items")
    
    # Сохраняем результат
    output = {
        "last_update": int(time.time()),
        "successful_items": len(prices),
        "failed_items": len(failed),
        "data": prices
    }
    
    with open("ambershire-prices-actions.json", "w") as f:
        json.dump(output, f, indent=2)
    
    print("Saved to ambershire-prices-actions.json")
    
    if failed:
        print(f"Failed items: {failed}")

if __name__ == "__main__":
    main()
