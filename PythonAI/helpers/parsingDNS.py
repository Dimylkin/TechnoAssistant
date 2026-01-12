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

construction_csv = ConstructionCSV("..\\dataset\\dataset_pc_from_dns.csv")

TARGET_ROWS = 300 - 91
PRODUCTS_PER_PAGE = 18
current_row_count = 0
list_page = [14, 6, 26, 19, 29]
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
            EC.presence_of_element_located((By.CLASS_NAME, 'product-buy__price'))
        )
        price_text = price_element.text.strip()
        data['price'] = int(price_text.replace('₽', '').replace(' ', '').strip())
        data['link'] = driver.current_url
        data['new'] = "yes"

        driver.execute_script("window.scrollTo(0, 2600);")
        time.sleep(uniform(1, 2))

        expand_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button.product-characteristics__expand"))
        )
        driver.execute_script("arguments[0].click();", expand_button)
        time.sleep(uniform(1, 2))

        specs = driver.find_elements(By.CLASS_NAME, 'product-characteristics__spec')

        for spec in specs:
            try:
                title = spec.find_element(By.CLASS_NAME, 'product-characteristics__spec-title').text.strip()
                value = spec.find_element(By.CLASS_NAME, 'product-characteristics__spec-value').text.strip()

                if "Операционная система" in title:
                    data['os'] = value
                elif "Модель процессора" in title:
                    data['model_cpu'] = value
                elif "Общее количество ядер" in title:
                    data['core'] = value
                elif "Максимальная частота производительных ядер" in title:
                    data['frequency_ghz'] = value
                elif "Сокет" in title:
                    data['socket'] = value
                elif "Общий объем оперативной памяти" in title:
                    data['ram_gb'] = value
                elif "Тип оперативной памяти" in title:
                    data['ram_type'] = value
                elif "Частота оперативной памяти" in title:
                    data['ram_ghz'] = value
                elif (("Модель интегрированной видеокарты" in title) or
                      ("Модель дискретной видеокарты" in title)) and value != "нет":
                    data['model_gpu'] = value
                elif "Объем видеопамяти" in title:
                    data['vram_gb'] = value
                elif "Конфигурация твердотельных накопителей (SSD)" in title:
                    matches = re.findall(r'(\d+)\s*(TB|GB)', value, re.IGNORECASE)
                    total_gb = sum(int(v) * (1024 if u.upper() == 'TB' else 1) for v, u in matches)
                    data['storage_gb'] = total_gb
                elif "Чипсет" in title:
                    data['mother_board'] = value
                elif "Мощность блока питания" in title:
                    data['power_supply'] = value[:4].replace(" ", "")
            except:
                continue

        return data

    except Exception as e:
        print(f"Ошибка парсинга товара: {e}")
        return None


while current_row_count < TARGET_ROWS:
    list_page.append(current_page)
    url = f'https://www.dns-shop.ru/catalog/17a8932c16404e77/personalnye-kompyutery/?p={current_page}'
    driver.get(url)
    print(f"\n=== Страница {current_page} ===")
    time.sleep(uniform(1, 2))

    products = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'catalog-product__name'))
    )

    print(f"Найдено товаров: {len(products)}")

    product_urls = []
    for product in products:
        try:
            href = product.get_attribute('href')
            if href and '/product/' in href:
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