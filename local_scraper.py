#!/usr/bin/env python3
"""
УНИВЕРСАЛЬНЫЙ СКРАПЕР ДЛЯ AMBERSHIRE (Turtle WoW)
Объединяет функциональность filtered_scraper.py и ambershire_full_scraper.py
Для локального запуска и ручной загрузки результатов в репозиторий
"""

import json
import time
import re
from typing import Dict, List, Set, Optional
import requests
from bs4 import BeautifulSoup

# ========== КОНФИГУРАЦИЯ ==========
MODE = "BOTH"  # "FILTERED", "FULL", или "BOTH" - для создания обоих файлов
DAYS_TO_ANALYZE = 7
REQUEST_DELAY = 0.3  # Задержка между запросами (секунды)

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
    
    # Consumables (полный список из твоего consumable_db.py)
    20748, 20747, 23123, 20749, 20750, 3829, 3824, 13447, 9187, 13445,
    5634, 17708, 13454, 7676, 13453, 12820, 5633, 5631, 12431, 12430,
    12436, 12433, 12435, 12432, 12434, 53015, 51717, 8956, 4623, 13455,
    61225, 3827, 6149, 13443, 13444, 13446, 3928, 9206, 21151, 21114,
    18262, 23122, 3387, 12217, 61423, 10646, 61175, 61174, 13461, 13460,
    13459, 13458, 13457, 13456, 6051, 6048, 6052, 6049, 6050, 61224,
    18641, 10507, 9088, 15993, 4390, 13928, 9179, 18253, 2456, 2459,
    9172, 3823, 19440, 6453, 6452, 54010, 20520, 20007, 60976, 60977,
    60978, 9144, 10307, 10310, 10306, 10305, 10308, 10309, 13462, 5823,
    13931, 3382, 3388, 20004, 3826, 9036, 2633, 20008, 83309, 3386,
    9224, 17407, 20002, 8951, 6662, 22682, 9155, 12404, 12643, 6373,
    21546, 9264, 61181, 84040, 13452, 50237, 51720, 13442, 13935, 84041,
    51718, 2091, 12190, 47410, 47412, 47414,
    
    # Дополнительные важные предметы
    3825, 13510, 13512, 13511, 13513, 19183, 4392, 16023, 5206, 1703,
    9030, 13506, 53015, 61225, 61181, 84040, 50237, 51720, 13442, 13935,
    84041, 51718, 2091, 12190, 47410, 47412, 47414
}

# Профессии для полного сканирования
PROFESSIONS = ["alchemy", "cooking", "enchanting", "engineering", "first-aid"]

# API endpoints
API_BASE = "https://api.wowauctions.net/items/stats/30d/ambershire/mergedAh/{itemid}"
PROFESSION_BASE_URL = "https://www.wowauctions.net/professions/turtle-wow/ambershire/mergedAh/{profession}"

# ========== ФУНКЦИИ ==========

def fetch_item_price(item_id: int, days: int = DAYS_TO_ANALYZE) -> Optional[int]:
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


def fetch_profession_items(profession: str) -> Set[int]:
    """Парсит страницу профессии и извлекает все itemID"""
    url = PROFESSION_BASE_URL.format(profession=profession)
    print(f"  Fetching {profession}...", end=" ")
    
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
        
        print(f"OK ({len(item_ids)} items)")
        return item_ids
        
    except Exception as e:
        print(f"ERROR: {e}")
        return set()


def run_filtered_scraper() -> Dict:
    """Запускает фильтрованный скрапер (только NEEDED_ITEMIDS)"""
    print("\n" + "="*70)
    print("🚀 ЗАПУСК ФИЛЬТРОВАННОГО СКРАПЕРА")
    print(f"Целевые предметы: {len(NEEDED_ITEMIDS)}")
    print("="*70)
    
    prices = {}
    failed = []
    successful = 0
    
    for idx, item_id in enumerate(sorted(NEEDED_ITEMIDS), 1):
        print(f"[{idx}/{len(NEEDED_ITEMIDS)}] Item {item_id}...", end=" ")
        
        price = fetch_item_price(item_id)
        
        if price is not None:
            prices[str(item_id)] = price
            successful += 1
            print(f"OK ({price} copper = {price/10000:.2f}g)")
        else:
            failed.append(item_id)
            print("NO DATA")
        
        time.sleep(REQUEST_DELAY)
    
    # Формируем результат
    result = {
        "last_update": int(time.time()),
        "total_items": len(NEEDED_ITEMIDS),
        "successful_items": successful,
        "failed_items": len(failed),
        "data": prices
    }
    
    print(f"\n✅ ФИЛЬТРОВАННЫЙ СКРАПЕР ЗАВЕРШЕН:")
    print(f"   Успешно: {successful}/{len(NEEDED_ITEMIDS)}")
    print(f"   Без данных: {len(failed)}")
    
    return result


def run_full_scraper() -> Dict:
    """Запускает полный скрапер (профессии + NEEDED_ITEMIDS)"""
    print("\n" + "="*70)
    print("🚀 ЗАПУСК ПОЛНОГО СКРАПЕРА")
    print("Сбор предметов из профессий + consumable_db.py")
    print("="*70)
    
    # Шаг 1: Собираем предметы из профессий
    print("\n[1/3] Сбор предметов из профессий...")
    profession_items = set()
    
    for profession in PROFESSIONS:
        items = fetch_profession_items(profession)
        profession_items.update(items)
        time.sleep(1)  # Rate limiting
    
    print(f"   Всего из профессий: {len(profession_items)} предметов")
    
    # Шаг 2: Добавляем недостающие из consumable_db.py
    print("\n[2/3] Добавление предметов из consumable_db.py...")
    all_items = profession_items.copy()
    missing_items = NEEDED_ITEMIDS - profession_items
    
    if missing_items:
        print(f"   Добавлено {len(missing_items)} предметов из consumable_db.py")
        all_items.update(missing_items)
    else:
        print("   Все предметы из consumable_db.py уже есть в профессиях!")
    
    print(f"   Всего для сканирования: {len(all_items)} предметов")
    
    # Шаг 3: Собираем цены
    print("\n[3/3] Сбор цен...")
    prices = {}
    failed = []
    successful = 0
    
    for idx, item_id in enumerate(sorted(all_items), 1):
        print(f"[{idx}/{len(all_items)}] Item {item_id}...", end=" ")
        
        price = fetch_item_price(item_id)
        
        if price is not None:
            prices[str(item_id)] = price
            successful += 1
            print(f"OK ({price} copper = {price/10000:.2f}g)")
        else:
            failed.append(item_id)
            print("NO DATA")
        
        time.sleep(REQUEST_DELAY)
    
    # Формируем результат
    result = {
        "last_update": int(time.time()),
        "total_items_scanned": len(all_items),
        "items_from_professions": len(profession_items),
        "items_added_from_consumable_db": len(missing_items),
        "successful_items": successful,
        "failed_items": len(failed),
        "data": prices
    }
    
    print(f"\n✅ ПОЛНЫЙ СКРАПЕР ЗАВЕРШЕН:")
    print(f"   Успешно: {successful}/{len(all_items)}")
    print(f"   Без данных: {len(failed)}")
    
    return result


def save_results(filtered_data: Dict = None, full_data: Dict = None):
    """Сохраняет результаты в JSON файлы"""
    print("\n" + "="*70)
    print("💾 СОХРАНЕНИЕ РЕЗУЛЬТАТОВ")
    print("="*70)
    
    files_saved = []
    
    if filtered_data:
        with open("ambershire-prices-filtered.json", "w", encoding='utf-8') as f:
            json.dump(filtered_data, f, indent=2, ensure_ascii=False)
        files_saved.append("ambershire-prices-filtered.json")
        print(f"✅ ambershire-prices-filtered.json - {len(filtered_data['data'])} предметов с ценами")
    
    if full_data:
        with open("ambershire-prices-full.json", "w", encoding='utf-8') as f:
            json.dump(full_data, f, indent=2, ensure_ascii=False)
        files_saved.append("ambershire-prices-full.json")
        print(f"✅ ambershire-prices-full.json - {len(full_data['data'])} предметов с ценами")
    
    # Сохраняем статистику
    stats = {
        "last_run": int(time.time()),
        "files_generated": files_saved,
        "mode": MODE
    }
    
    with open("scraper_stats.json", "w", encoding='utf-8') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    
    print(f"\n📊 Статистика сохранена в scraper_stats.json")
    print("🎯 Теперь можно загрузить файлы в репозиторий вручную")


def main():
    """Основная функция"""
    print("="*70)
    print("🎯 УНИВЕРСАЛЬНЫЙ СКРАПЕР AMBERSHIRE (Turtle WoW)")
    print("   Для локального запуска и ручной загрузки в репозиторий")
    print("="*70)
    
    start_time = time.time()
    filtered_data = None
    full_data = None
    
    try:
        # Выбираем режим работы
        if MODE == "FILTERED" or MODE == "BOTH":
            filtered_data = run_filtered_scraper()
        
        if MODE == "FULL" or MODE == "BOTH":
            full_data = run_full_scraper()
        
        # Сохраняем результаты
        save_results(filtered_data, full_data)
        
        # Итоговая статистика
        total_time = time.time() - start_time
        print(f"\n⏱️  Общее время выполнения: {total_time:.1f} секунд")
        print("✅ ВСЕ ЗАДАЧИ ВЫПОЛНЕНЫ!")
        
    except KeyboardInterrupt:
        print(f"\n❌ Скрапер остановлен пользователем")
    except Exception as e:
        print(f"\n❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()