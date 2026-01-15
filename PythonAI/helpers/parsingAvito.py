import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from random import uniform, randint
import re

from constructionCSV import ConstructionCSV

def create_driver():
    """Создание драйвера с максимальной маскировкой"""
    options = uc.ChromeOptions()

    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-web-security')
    options.add_argument('--disable-features=IsolateOrigins,site-per-process')

    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')

    options.add_argument('--window-size=1920,1080')

    options.add_argument('--lang=ru-RU')

    driver = uc.Chrome(options=options, use_subprocess=True)

    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    })

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    driver.execute_cdp_cmd('Emulation.setLocaleOverride', {'locale': 'ru-RU'})

    return driver

driver = create_driver()

construction_csv = ConstructionCSV("..\\dataset\\dataset_pc_from_avito.csv")

TARGET_ROWS = 300
current_row_count = 0
list_page = []
current_page = randint(1, 31)

def parse_product():
    """Парсинг одного товара"""
    data = {
        "price": None, "os": None, "new": "yes", "model_cpu": None,
        "core": None, "frequency_ghz": None, "socket": None,
        "ram_gb": None, "ram_type": None, "ram_ghz": None,
        "model_gpu": None, "vram_gb": None, "storage_gb": None,
        "mother_board": None, "power_supply": None, "estimation": None,
        "link": None
    }

    try:
        price_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-marker="item-view/item-price"]'))
        )

        price_text = driver.execute_script("return arguments[0].textContent;", price_element).strip()

        data['price'] = int(price_text.replace('\xa0', '').replace('₽', '').replace(' ', '').strip())
        data['link'] = driver.current_url

        driver.execute_script("window.scrollTo(0, 800);")
        time.sleep(uniform(3, 5))

        params_list = driver.find_element(By.CSS_SELECTOR, 'ul.params__paramsList___XzY3MG')
        param_items = params_list.find_elements(By.CSS_SELECTOR, 'li.params__paramsList__item___XzY3MG')

        params = {}
        for item in param_items:
            full_text = item.text.strip()
            try:
                parts = full_text.split(':', 1)
                if len(parts) == 2:
                    title = parts[0].strip()
                    value = parts[1].strip()
                    params[title] = value
            except:
                continue

        for title, value in params.items():
            try:
                if "Состояние" in title:
                    if value == "Б/у":
                        data['new'] = "no"
                    if value == "Новое":
                        data['new'] = "yes"
                elif "Процессор" in title:
                    data['model_cpu'] = value
                elif "Оперативная память" in title:
                    data['ram_gb'] = value
                elif "Видеокарта" in title:
                    data['model_gpu'] = value
                elif "Материнская плата" in title:
                    data['mother_board'] = value
            except:
                continue

        return data

    except Exception as e:
        print(f"Ошибка парсинга товара: {e}")
        return None


while current_row_count < TARGET_ROWS:
    list_page.append(current_page)
    url = f'https://www.avito.ru/all/nastolnye_kompyutery/sistemnye_bloki-ASgBAgICAUS02xKMqY0D?cd=1&p={current_page}'
    driver.get(url)
    print(f"\n=== Страница {current_page} ===")
    time.sleep(uniform(1, 2))

    for scroll_step in range(15):
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(uniform(0.5, 1))

    products = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[data-marker="item-title"]'))
    )

    print(f"Найдено товаров: {len(products)}")

    product_urls = []
    for product in products:
        try:
            href = product.get_attribute('href')
            if href and href != None:
                product_urls.append(href)
        except:
            continue

    for i, product_url in enumerate(product_urls):
        if current_row_count >= TARGET_ROWS:
            break

        print(f"\n[{current_row_count + 1}/{TARGET_ROWS}] Обрабатываю товар {i + 1}...")

        driver.get(product_url)
        print(f"✓ Перешли на товар: {driver.current_url}")
        time.sleep(uniform(3, 5))

        product_data = parse_product()

        if product_data and product_data['price']:
            construction_csv.add_row(product_data)
            current_row_count += 1
            print(f"✓ Товар добавлен. Цена: {product_data['price']} руб")
        else:
            print("✗ Товар пропущен (нет данных)")

        time.sleep(uniform(1, 2))


    while (True):
        rand_page = randint(1, 31)
        if rand_page not in list_page:
            current_page = rand_page
            break

driver.quit()
print(f"\n=== Парсинг завершен. Собрано {current_row_count} товаров ===")