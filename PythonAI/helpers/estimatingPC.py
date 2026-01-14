import re
import pandas as pd
from constructionCSV import ConstructionCSV


class EstimatingPC:
    def __init__(self, dataset_file_path):
        self.dataset_file_path = dataset_file_path
        self.dataset = ConstructionCSV(dataset_file_path).open_csv()[1:]

        self.estimating()

    @staticmethod
    def check_modern(cpu):
        if pd.notna(cpu):
            old_cpu_list = ['core', 'atom', 'xeon', 'pentium', 'celeron',
                            'athlon', 'a4', 'a6', 'a8', 'a10', 'a12', 'fx',
                            'phenom', 'sun']
            for old_cpu in old_cpu_list:
                if old_cpu in cpu:
                    if old_cpu == "core":
                        if "core 2" in cpu or "core q" in cpu:
                            return False
                        elif "ultra" in cpu:
                            return True
                        else:
                            match = re.search(r'[iI]([3579])[- ](\d{4,5})', cpu)
                            if not match:
                                return False
                            model_number = match.group(2)

                            if len(model_number) == 5:
                                return True
                            elif len(model_number) == 4:
                                return False
                            else:
                                return False

                    if old_cpu == "pentium":
                        if "pentium gold" in cpu:
                            return False

                    if old_cpu == "celeron":
                        if "celeron n" in cpu:
                            return False

                    if old_cpu == "athlon":
                        if "athlon gold" in cpu or "athlon silver" in cpu or "athlon 3" in cpu:
                            return False
                    return False
            return True
        return False

    @staticmethod
    def check_cpu(cpu, core, frequency_ghz):
        cpu_score = 0
        cpu_small_list = ['pentium', 'celeron', 'athlon', 'n100', 'n200']
        cpu_low_list = ['i3', 'ryzen 3']
        cpu_mid_list = ['i5', 'ryzen 5']
        cpu_hid_list = ['i7', 'ryzen 7', 'm2']
        cpu_ex_list = ['i9', 'ryzen 9', 'm4']

        if core <= 4.0:
            cpu_score += 0.5
        elif 4.0 < core <= 8.0:
            cpu_score += 1
        elif 8.0 < core <= 12.0:
            cpu_score += 1.5
        elif 12.0 < core <= 16.0:
            cpu_score += 2
        elif 16.0 < core <= 20.0:
            cpu_score += 2.5
        elif core > 20.0:
            cpu_score += 3

        if frequency_ghz <= 800.0:
            cpu_score += 0
        elif 800.0 < frequency_ghz <= 3200.0:
            cpu_score += 1
        elif 3200.0 < frequency_ghz <= 4800.0:
            cpu_score += 2
        elif frequency_ghz > 4800:
            cpu_score += 3

        if pd.isna(cpu):
            return 0.0

        for cpu_small in cpu_small_list:
            if cpu_small in cpu:
                cpu_score += 1
                break

        for cpu_low in cpu_low_list:
            if cpu_low in cpu:
                cpu_score += 2
                break

        for cpu_mid in cpu_mid_list:
            if cpu_mid in cpu:
                cpu_score += 1
                break

        for cpu_hid in cpu_hid_list:
            if cpu_hid in cpu:
                cpu_score += 3
                break

        for cpu_ex in cpu_ex_list:
            if cpu_ex in cpu:
                cpu_score += 4
                break

        return min(cpu_score, 10.0)

    @staticmethod
    def check_gpu(gpu, vram_gb):
        """
        Оценить видеокарту (максимум 10 баллов)

        Учитывает: поколение карты, модель и объём VRAM
        """
        if pd.isna(gpu):
            return 0.0

        gpu_lower = str(gpu).lower().strip()
        gpu_score = 0.0

        # Нет видеокарты
        if "без" in gpu_lower or "graphics" in gpu_lower:
            if vram_gb <= 0.0:
                return 0.5  # Интегрированная графика
            else:
                return 1.0

        # === NVIDIA ===
        if 'rtx 50' in gpu_lower:
            if '5090' in gpu_lower:
                gpu_score = 10.0
            elif '5080' in gpu_lower:
                gpu_score = 9.5
            elif '5070' in gpu_lower:
                gpu_score = 9
            elif '5060' in gpu_lower:
                gpu_score = 8

        if 'rtx 40' in gpu_lower:
            if '4090' in gpu_lower:
                gpu_score = 9.5
            elif '4080' in gpu_lower:
                gpu_score = 9.0
            elif '4070' in gpu_lower:
                gpu_score = 8.5
            elif '4060' in gpu_lower:
                gpu_score = 7.5

        if 'rtx 30' in gpu_lower:
            if '3090' in gpu_lower:
                gpu_score = 8
            elif '3080' in gpu_lower:
                gpu_score = 7.5
            elif '3070' in gpu_lower:
                gpu_score = 6.5
            elif '3060' in gpu_lower:
                gpu_score = 6.0
            elif '3050' in gpu_lower:
                gpu_score = 5.0

        if 'rtx 20' in gpu_lower:
            if '2080' in gpu_lower:
                gpu_score = 6.5
            elif '2070' in gpu_lower:
                gpu_score = 5.5
            elif '2060' in gpu_lower:
                gpu_score = 4.5

        if 'gtx 16' in gpu_lower:
            if '1660' in gpu_lower:
                gpu_score = 3.5
            elif '1650' in gpu_lower:
                gpu_score = 3.25

        if 'gtx 10' in gpu_lower:
            if '1080' in gpu_lower:
                gpu_score = 3
            elif '1070' in gpu_lower:
                gpu_score = 2.5
            elif '1060' in gpu_lower:
                gpu_score = 2
            elif '1050' in gpu_lower:
                gpu_score = 1.5

        if 'gtx 9' in gpu_lower:
            if '980' in gpu_lower or '970' in gpu_lower:
                gpu_score = 1.5
            elif '960' in gpu_lower or '950' in gpu_lower:
                gpu_score = 1
            elif 'gtx' in gpu_lower:
                gpu_score = 0.5

        # === AMD ===

        # RX 7000 Series (2022-2024) - Топовые
        if 'rx 7' in gpu_lower:
            if '7900' in gpu_lower:
                gpu_score = 9.5
            elif '7800' in gpu_lower:
                gpu_score = 8.5
            elif '7700' in gpu_lower:
                gpu_score = 7.5
            elif '7600' in gpu_lower:
                gpu_score = 6.5

        if 'rx 6' in gpu_lower:
            if '6950' in gpu_lower or '6900' in gpu_lower:
                gpu_score = 8.0
            elif '6800' in gpu_lower:
                gpu_score = 7.5
            elif '6700' in gpu_lower:
                gpu_score = 6.5
            elif '6600' in gpu_lower:
                gpu_score = 5.5
            elif '6500' in gpu_lower:
                gpu_score = 4.0
            elif '6400' in gpu_lower:
                gpu_score = 3.0

        if 'rx 5' in gpu_lower:
            if '5700' in gpu_lower:
                gpu_score = 5.0
            elif '5600' in gpu_lower:
                gpu_score = 4.5
            elif '5500' in gpu_lower:
                gpu_score = 3.5

        if 'vega' in gpu_lower:
            if 'radeon vii' in gpu_lower or 'radeon 7' in gpu_lower:
                gpu_score = 5.0
            elif '64' in gpu_lower and 'rx' in gpu_lower:
                gpu_score = 4.0
            elif '56' in gpu_lower and 'rx' in gpu_lower:
                gpu_score = 3.5
            elif 'vega' in gpu_lower and any(x in gpu_lower for x in ['11', '10', '8', '7', '6', '3']):
                gpu_score = 0.5  # Интегрированная Vega

        elif 'rx 590' in gpu_lower:
            gpu_score = 3.0
        elif 'rx 580' in gpu_lower or 'rx 570' in gpu_lower:
            gpu_score = 2.5
        elif 'rx 560' in gpu_lower or 'rx 550' in gpu_lower:
            gpu_score = 1.5

        # R9/R7/R5 Series (2013-2016) - Устаревшие
        elif 'r9 290' in gpu_lower or 'r9 390' in gpu_lower or 'r9 fury' in gpu_lower:
            gpu_score = 2.0
        elif 'r9' in gpu_lower:
            gpu_score = 1.5
        elif 'r7' in gpu_lower:
            gpu_score = 1.0
        elif 'r5' in gpu_lower:
            gpu_score = 0.5
        elif 'r3' in gpu_lower or 'r4' in gpu_lower:
            gpu_score = 0.0  # Интегрированная

        # Бонус за VRAM
        if vram_gb >= 16:
            gpu_score += 0.5
        elif vram_gb >= 12:
            gpu_score += 0.3
        elif vram_gb >= 8:
            gpu_score += 0.2

        return min(gpu_score, 10.0)

    @staticmethod
    def check_ram(type_ram, ghz, gb):
        """
        Оценить ОЗУ (максимум 10 баллов)

        Распределение баллов:
        - Объём RAM: до 6 баллов (60%)
        - Тип RAM: до 2 баллов (20%)
        - Частота RAM: до 2 баллов (20%)
        """
        try:
            if pd.notna(type_ram):
                type_ram = str(type_ram).lower().strip()
            else:
                type_ram = ""

            if pd.notna(ghz):
                ghz = float(ghz)
            else:
                ghz = 0.0

            if pd.notna(gb):
                gb = float(gb)
            else:
                gb = 0.0
        except Exception as e:
            print(f"Ошибка преобразования RAM: {e}")
            return 0.0

        ram_score = 0.0

        # Проверка на устаревшую память
        if "ddr1" in type_ram or "ddr2" in type_ram:
            return 0.0

        # 1. ОЦЕНКА ОБЪЁМА (60% = 6 баллов)
        if gb >= 64:
            capacity_score = 6.0
        elif gb >= 32:
            capacity_score = 5.0
        elif gb >= 16:
            capacity_score = 3.5
        elif gb >= 8:
            capacity_score = 2.0
        elif gb >= 4:
            capacity_score = 0.5
        else:
            capacity_score = 0.0

        ram_score += capacity_score

        # 2. ОЦЕНКА ТИПА RAM (20% = 2 балла)
        if "ddr5" in type_ram or "lpddr5" in type_ram:
            type_score = 2.0
        elif "ddr4" in type_ram or "lpddr4" in type_ram:
            type_score = 1.0
        elif "ddr3" in type_ram or "lpddr3" in type_ram:
            type_score = 0.2
        else:
            type_score = 0.0

        ram_score += type_score

        # 3. ОЦЕНКА ЧАСТОТЫ (20% = 2 балла)
        frequency_score = 0.0

        if "ddr5" in type_ram or "lpddr5" in type_ram:
            if ghz >= 7200:
                frequency_score = 2.0
            elif ghz >= 6400:
                frequency_score = 1.5
            elif ghz >= 6000:
                frequency_score = 1.2
            elif ghz >= 5600:
                frequency_score = 1.0
            elif ghz >= 5200:
                frequency_score = 0.7
            elif ghz >= 4800:
                frequency_score = 0.5
            else:
                frequency_score = 0.2

        elif "ddr4" in type_ram or "lpddr4" in type_ram:
            if ghz >= 4000:
                frequency_score = 2.0
            elif ghz >= 3600:
                frequency_score = 1.5
            elif ghz >= 3200:
                frequency_score = 1.2
            elif ghz >= 2666:
                frequency_score = 0.8
            elif ghz >= 2400:
                frequency_score = 0.6
            elif ghz >= 2133:
                frequency_score = 0.4
            elif ghz >= 1600:
                frequency_score = 0.2
            else:
                frequency_score = 0.0

        elif "ddr3" in type_ram or "lpddr3" in type_ram:
            if ghz >= 2400:
                frequency_score = 1.0
            elif ghz >= 1866:
                frequency_score = 0.7
            elif ghz >= 1600:
                frequency_score = 0.5
            elif ghz >= 1333:
                frequency_score = 0.3
            elif ghz >= 800:
                frequency_score = 0.2
            else:
                frequency_score = 0.0

        ram_score += frequency_score

        return min(ram_score, 10.0)

    @staticmethod
    def check_mb(mb, socket):
        """
        Оценить материнскую плату (максимум 5 баллов)

        Оценивает по чипсету и сокету
        """
        if pd.isna(mb) and pd.isna(socket):
            return 0.0

        mb_lower = str(mb).lower().strip() if pd.notna(mb) else ""
        socket_lower = str(socket).lower().strip() if pd.notna(socket) else ""

        mb_score = 0.0

        # === ОЦЕНКА ПО ЧИПСЕТУ (3 балла) ===

        # Intel - Актуальные чипсеты
        if any(chip in mb_lower for chip in ['z890', 'z790', 'z690']):
            mb_score += 3.0  # Топовые Z-серии
        elif any(chip in mb_lower for chip in ['b760', 'b660', 'h770', 'h670']):
            mb_score += 2.5  # Средние современные
        elif any(chip in mb_lower for chip in ['h610', 'h510', 'b560']):
            mb_score += 2.0  # Бюджетные современные

        # Intel - Устаревающие
        elif any(chip in mb_lower for chip in ['z590', 'z490', 'b460', 'h470']):
            mb_score += 1.5
        elif any(chip in mb_lower for chip in ['z390', 'z370', 'h370', 'b360', 'h310']):
            mb_score += 1.0

        # Intel - Старые
        elif any(chip in mb_lower for chip in ['z270', 'z170', 'h270', 'h110', 'b250']):
            mb_score += 0.5
        elif any(chip in mb_lower for chip in ['z97', 'z87', 'h97', 'h87', 'b85', 'h81']):
            mb_score += 0.2

        # Intel - Очень старые
        elif any(chip in mb_lower for chip in ['x79', 'x99', 'x299']):
            mb_score += 0.5  # HEDT платформы
        elif any(chip in mb_lower for chip in ['h61', 'h67', 'p67', 'z68']):
            mb_score += 0.0

        # AMD - Актуальные чипсеты
        elif any(chip in mb_lower for chip in ['x870', 'x670', 'b650', 'a620']):
            mb_score += 3.0  # AM5 платформа (DDR5)
        elif any(chip in mb_lower for chip in ['x570', 'b550', 'a520']):
            mb_score += 2.5  # AM4 топовые
        elif 'b450' in mb_lower:
            mb_score += 2.0  # AM4 средние
        elif any(chip in mb_lower for chip in ['a320', 'b350', 'x370']):
            mb_score += 1.5  # AM4 старые

        # AMD - Устаревшие
        elif any(chip in mb_lower for chip in ['a88x', 'a78', 'a68', 'a58']):
            mb_score += 0.5
        elif any(chip in mb_lower for chip in ['990fx', '970', '880g']):
            mb_score += 0.2

        # Если чипсет не определён, но есть название платы
        elif mb_lower and mb_lower not in ['null', 'amd', 'intel']:
            mb_score += 1.0  # Минимум за наличие платы

        # === ОЦЕНКА ПО СОКЕТУ (2 балла) ===

        # Intel - Современные сокеты
        if 'lga 1851' in socket_lower:
            mb_score += 2.0  # LGA 1851 (Arrow Lake, 2024+)
        elif 'lga 1700' in socket_lower:
            mb_score += 1.8  # LGA 1700 (12-14 gen, 2021-2024)
        elif 'lga 1200' in socket_lower:
            mb_score += 1.5  # LGA 1200 (10-11 gen, 2020-2021)

        # Intel - Устаревшие сокеты
        elif 'lga 1151' in socket_lower:
            mb_score += 1.0  # LGA 1151 (6-9 gen)
        elif 'lga 1150' in socket_lower or 'lga 1155' in socket_lower:
            mb_score += 0.5  # Старые
        elif 'lga 2011' in socket_lower or 'lga 2066' in socket_lower:
            mb_score += 0.8  # HEDT платформы

        # AMD - Современные сокеты
        elif 'am5' in socket_lower:
            mb_score += 2.0  # AM5 (Ryzen 7000+, DDR5, 2022+)
        elif 'am4' in socket_lower:
            mb_score += 1.5  # AM4 (Ryzen 1000-5000, 2017-2022)

        # AMD - Устаревшие сокеты
        elif 'am3' in socket_lower or 'am3+' in socket_lower:
            mb_score += 0.5
        elif 'fm2' in socket_lower or 'fm2+' in socket_lower:
            mb_score += 0.3

        # Мобильные сокеты (BGA - распаянные)
        elif any(bga in socket_lower for bga in ['bga 2049', 'bga 1744', 'bga 1449']):
            mb_score += 1.0  # Современные мобильные
        elif 'bga' in socket_lower:
            mb_score += 0.5  # Старые мобильные

        # Мобильные сокеты AMD (FP)
        elif any(fp in socket_lower for fp in ['fp7', 'fp8']):
            mb_score += 1.5  # Современные AMD мобильные
        elif any(fp in socket_lower for fp in ['fp5', 'fp6']):
            mb_score += 1.0

        return min(mb_score, 5.0)

    @staticmethod
    def check_storage(storage):
        if storage < 120.0:
            return 0
        elif 120.0 <= storage <= 240.0:
            return 1
        elif 240.0 < storage <= 500.0:
            return 2
        elif 500.0 < storage <= 1000.0:
            return 3
        elif 1000.0 < storage <= 2050.0:
            return 4
        elif storage > 2050.0:
            return 5
        else:
            return 0

    @staticmethod
    def check_power(power):
        if power < 100.0:
            return 0
        elif 100.0 <= power <= 250.0:
            return 1
        elif 250.0 < power <= 400.0:
            return 2
        elif 400.0 < power <= 550.0:
            return 3
        elif 550.0 < power <= 850.0:
            return 4
        elif power > 850.0:
            return 5
        else:
            return 0

    @staticmethod
    def check_price(price, general_score, new, os):
        """
        Оценить соотношение цена/качество

        Параметры:
        - price: цена в рублях
        - general_score: общий балл ПК (сумма всех оценок, макс ~50)
        - new: состояние ("yes"/"no")
        - os: операционная система

        Возвращает: "Отличная цена" / "Хорошая цена" / "Приемлемо" / "Дорого" / "Очень дорого"
        """
        try:
            if pd.notna(price):
                price = float(price)
            else:
                return "Нет данных о цене"

            if pd.notna(new):
                new_lower = str(new).lower().strip()
            else:
                new_lower = "no"

            if pd.notna(os):
                os_lower = str(os).lower().strip()
            else:
                os_lower = ""
        except Exception as e:
            print(f"Ошибка в check_price: {e}")
            return "Ошибка данных"

        # Коэффициент для б/у (скидка 20-30%)
        condition_multiplier = 1.0 if new_lower == "yes" else 0.90

        # Штраф за отсутствие ОС или FreeDOS
        os_penalty = 0
        if os_lower in ['null', 'freedos', 'dos', '']:
            os_penalty = 3000

        # Расчёт ожидаемой цены на основе баллов
        # Максимум баллов: CPU(10) + GPU(10) + RAM(10) + MB(5) + Storage(5) + Power(5) = 45
        if general_score >= 40:
            expected_price = 350000  # Топовая сборка
        elif general_score >= 35:
            expected_price = 250000  # Высокий уровень
        elif general_score >= 30:
            expected_price = 150000  # Средне-высокий
        elif general_score >= 25:
            expected_price = 120000  # Средний
        elif general_score >= 20:
            expected_price = 80000  # Ниже среднего
        elif general_score >= 15:
            expected_price = 60000  # Бюджетный
        elif general_score >= 10:
            expected_price = 30000  # Слабый
        else:
            expected_price = 12000  # Офисный

        # Применить коэффициенты
        expected_price *= condition_multiplier
        expected_price += os_penalty

        # Соотношение реальной цены к ожидаемой
        price_ratio = price / expected_price if expected_price > 0 else 999

        # Оценка
        if price_ratio <= 0.8:
            return "Хорошая"
        elif price_ratio <= 1.1:
            return "Нормальная"
        elif price_ratio <= 1.3:
            return "Плохая"
        else:
            return "Плохая"

    @staticmethod
    def get_number(number_string):
        try:
            if pd.notna(number_string):
                return float(number_string)
            else:
                return 0.0
        except Exception as e:
            print(f"Ошибка преобразования числа: {e}")
            return 0.0

    def estimating(self):
        """Оценка всех ПК в датасете"""
        df = pd.read_csv(self.dataset_file_path)

        for i in range(len(df)):
            pc = df.iloc[i]

            # Проверка на современность процессора
            # if not self.check_modern(pc['model_cpu']):
            #     df.loc[i, 'estimation'] = "Старый"
            #     continue

            # Получение числовых параметров
            cpu_core = self.get_number(pc['core'])
            cpu_ghz = self.get_number(pc['frequency_ghz'])
            gpu_vram = self.get_number(pc['vram_gb'])
            ram_ghz = self.get_number(pc['ram_ghz'])
            ram_gb = self.get_number(pc['ram_gb'])
            storage_gb = self.get_number(pc['storage_gb'])
            power = self.get_number(pc['power_supply'])

            # Оценка компонентов
            cpu_score = self.check_cpu(pc['model_cpu'], cpu_core, cpu_ghz)
            gpu_score = self.check_gpu(pc['model_gpu'], gpu_vram)
            ram_score = self.check_ram(pc['ram_type'], ram_ghz, ram_gb)
            mb_score = self.check_mb(pc['mother_board'], pc['socket'])
            storage_score = self.check_storage(storage_gb)
            power_score = self.check_power(power)

            # Общий балл
            general_score = cpu_score + gpu_score + ram_score + mb_score + storage_score + power_score

            # Оценка цены
            estimation = self.check_price(pc['price'], general_score, pc['new'], pc['os'])

            # Сохранение результатов
            df.loc[i, 'estimation'] = estimation
            df.loc[i, 'general_score'] = round(general_score, 2)

            # Вывод прогресса
            if (i + 1) % 100 == 0:
                print(f"Обработано {i + 1}/{len(df)} ПК...")

        df.to_csv(self.dataset_file_path, index=False)
        print(f"✓ Оценено {len(df)} ПК. Результаты сохранены.")

# Запуск
est = EstimatingPC("..\\dataset\\dataset_test.csv")
pc = {
    'price': '',
    'os': '',
    'new': '',
    'model_cpu': '',
    'core': '',
    'frequency_ghz': '',
    'socket': '',
    'ram_gb': '',
    'ram_type': '',
    'ram_ghz': '',
    'model_gpu': '',
    'vram_gb': '',
    'storage_gb': '',
    'mother_board': '',
    'power_supply': '',
}
est.estimating()
