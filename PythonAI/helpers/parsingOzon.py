import re

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
from random import uniform

from PythonAI.helpers.constructionCSV import ConstructionCSV

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

    driver = uc.Chrome(options=options, version_main=143)

    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
        "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
    })

    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    driver.execute_cdp_cmd('Emulation.setLocaleOverride', {'locale': 'ru-RU'})

    return driver

def parse_product():
    """Парсинг одного товара"""
    data = {
        "price": None, "os": None, "new": None, "model_cpu": None,
        "core": None, "frequency_ghz": None, "socket": None,
        "ram_gb": None, "ram_type": None, "ram_ghz": None,
        "model_gpu": None, "vram_gb": None, "storage_gb": None,
        "mother_board": None, "power_supply": None, "estimation": None,
        "link": None
    }

    try:
        price_container = driver.find_element(By.CLASS_NAME, 'pdp_bf9')

        price_span = price_container.find_element(By.CLASS_NAME, 'tsHeadline600Large')
        price_text = price_span.text.strip()

        price_clean = re.sub(r'\D', '', price_text)
        data['price'] = int(price_clean)
        data['link'] = driver.current_url

        for scroll_step in range(4):
            driver.execute_script("window.scrollBy(0, 950);")
            time.sleep(uniform(0.5, 1))

        titles = driver.find_elements(By.CLASS_NAME, 'pdp_a5i')
        values = driver.find_elements(By.CLASS_NAME, 'pdp_ai5')

        for title, value in zip(titles, values):
            title = title.text
            value = value.text

            if "ОС (краткое название)" in title:
                data['os'] = value
            elif "Процессор" in title:
                data['model_cpu'] = value
            elif "Число ядер процессора" in title:
                data['core'] = value
            elif "Частота процессора, ГГц" in title:
                data['frequency_ghz'] = value
            elif "Сокет" in title:
                data['socket'] = value
            elif "Оперативная память" in title:
                data['ram_gb'] = value
            elif "Тип памяти" in title:
                data['ram_type'] = value
            elif "Частота процессора, ГГц" in title:
                data['ram_ghz'] = value
            elif "Видеокарта" in title:
                data['model_gpu'] = value
            elif "Видеопамять" in title:
                data['vram_gb'] = value
            elif "Суммарный объем всех дисков, ГБ" in title:
                data['storage_gb'] = value
            elif "Чипсет" in title:
                data['mother_board'] = value
            elif "Мощность блока питания, Вт" in title:
                data['power_supply'] = value

        return data

    except Exception as e:
        print(f"Ошибка парсинга товара: {e}")
        return None

construction_csv = ConstructionCSV("..\\dataset\\dataset_pc_from_ozon_with_only_intel_i7_amd_r7.csv")
construction_csv.create_csv()

driver = create_driver()

url_with_only_intel_xeon = "https://www.ozon.ru/category/sistemnye-bloki-15704/?cpumodel=83018%2C100256425%2C100256427%2C100256424&opened=cpumodel%2Ccpuname"
url_with_only_amd_a = "https://www.ozon.ru/category/sistemnye-bloki-15704/?cpumodel=83002%2C82999%2C83007%2C83001%2C83000&opened=cpumodel%2Ccpuname"
url_with_only_intel_celeron_atom_and_other = "https://www.ozon.ru/category/sistemnye-bloki-15704/?cpumodel=83017%2C83010%2C100256419%2C83003%2C100258397%2C100256429%2C83009&opened=cpuname%2Ccpumodel"
url_with_only_intel_i3_amd_r3 = "https://www.ozon.ru/category/sistemnye-bloki-15704/?cpuname=179184%2C174141%2C326201%2C174136%2C336366%2C174072%2C339029%2C324274%2C339421%2C275953%2C100225467%2C174148%2C320739%2C339030%2C277433%2C339441%2C100225576%2C174159%2C339420%2C100225502%2C174071%2C325629%2C319312%2C100373591%2C100174292%2C100526389%2C174144%2C279870%2C100225462%2C100225503%2C100225593%2C337606%2C100863712%2C174133%2C174142%2C178359&opened=cpumodel%2Ccpuname"
url_with_only_intel_i5_amd_r5 = "https://www.ozon.ru/category/sistemnye-bloki-15704/?cpuname=174169%2C314525%2C174211%2C100225421%2C319510%2C174087%2C338763%2C100225384%2C100225419%2C338350%2C100225387%2C174198%2C174201%2C100225547%2C336178%2C174209%2C174177%2C338053%2C174163%2C100174195%2C174083%2C174097%2C320774%2C100225610%2C174167%2C174089%2C336576%2C100225577%2C174180%2C100225500%2C174182%2C174171%2C319511%2C100225425%2C335910%2C324005%2C174214%2C100427744%2C276261%2C100422026%2C100225591%2C276334%2C100143551%2C279869%2C100225385%2C100225370%2C336177%2C174188%2C174203%2C174173%2C174216&opened=cpuname%2Ccpumodel"
url_with_only_intel_i7_amd_r7 = "https://www.ozon.ru/category/sistemnye-bloki-15704/?cpuname=174237%2C269419%2C174228%2C174238%2C282610%2C174226%2C174221%2C100225297%2C100225229%2C320775%2C335929%2C100225614%2C100225218%2C174246%2C174248%2C100225215%2C100225214%2C174247%2C100225219%2C100794273%2C100225613%2C100225220%2C311168%2C174239%2C174229%2C100225568%2C174249&opened=cpumodel%2Ccpuname"
current_width = 0
current_row_count = 0

url = url_with_only_intel_i7_amd_r7
driver.get(url)
print("Открыл каталог")
time.sleep(uniform(5, 8))

for scroll_step in range(15):
    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(uniform(0.5, 1))

time.sleep(3)

products = driver.find_elements(By.CSS_SELECTOR, 'a.tile-clickable-element')
print(f"Найдено {len(products)} товаров на странице")

product_urls = []
for product in products:
    try:
        href = product.get_attribute('href')
        if href and '/product/' in href:
            product_urls.append(href)
    except:
        continue

product_urls = list(dict.fromkeys(product_urls))
print(f"Уникальных товаров для обработки: {len(product_urls)}")

for i, product_url in enumerate(product_urls):
    if current_row_count >= len(product_urls):
        break

    print(f"\n[{current_row_count + 1}/{len(product_urls)}] Обрабатываю товар {i + 1}")

    try:
        driver.get(product_url)
        print(f"✓ Перешли на товар: {driver.current_url}")
        time.sleep(uniform(3, 5))

        construction_csv.add_row(parse_product())

        current_row_count += 1
        print(f"✓ Товар обработан ({current_row_count}/{len(product_urls)})")
        driver.back()
        time.sleep(uniform(3, 5))

        if current_row_count % 10 == 0 and current_row_count > 0:
            pause = uniform(15, 30)
            print(f"⏸️ Пауза {pause:.0f} сек")
            time.sleep(pause)

    except Exception as e:
        print(f"✗ Ошибка: {e}")
        driver.get(url)
        time.sleep(3)
        continue

driver.quit()
print(f"\n=== Завершено. Обработано {current_row_count} товаров ===")
