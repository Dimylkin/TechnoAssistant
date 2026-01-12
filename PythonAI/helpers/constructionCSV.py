import csv
import os


class ConstructionCSV:
    def __init__(self, base_path_to_data_set):
        self.base_path_to_data_set = base_path_to_data_set

    def create_csv(self):
        """Создаёт CSV файл с заголовками"""
        # Создаём папку, если её нет
        os.makedirs(os.path.dirname(self.base_path_to_data_set), exist_ok=True)

        with open(self.base_path_to_data_set, mode='w', newline='', encoding='utf-8') as dataset_file:
            dataset_writer = csv.writer(dataset_file)
            dataset_writer.writerow([
                "price",
                "os",
                "new",
                "model_cpu",
                "core",
                "frequency_ghz",
                "socket",
                "ram_gb",
                "ram_type",
                "ram_ghz",
                "model_gpu",
                "vram_gb",
                "storage_gb",
                "mother_board",
                "power_supply",
                "estimation",
                "link"
            ])

    def add_row(self, data):
        """Добавляет одну строку в конец файла"""
        with open(self.base_path_to_data_set, mode='a', newline='', encoding='utf-8') as dataset_file:
            dataset_writer = csv.writer(dataset_file)

            # Преобразуем словарь в список значений (ПОРЯДОК ДОЛЖЕН СОВПАДАТЬ С ЗАГОЛОВКАМИ)
            row = [
                data.get("price", ""),
                data.get("os", ""),
                data.get("new", ""),
                data.get("model_cpu", ""),
                data.get("core", ""),
                data.get("frequency_ghz", ""),
                data.get("socket", ""),
                data.get("ram_gb", ""),
                data.get("ram_type", ""),
                data.get("ram_ghz", ""),
                data.get("model_gpu", ""),
                data.get("vram_gb", ""),
                data.get("storage_gb", ""),
                data.get("mother_board", ""),
                data.get("power_supply", ""),
                data.get("estimation", ""),
                data.get("link", "")
            ]
            dataset_writer.writerow(row)

    def add_rows(self, rows_list):
        """Добавляет несколько строк в конец файла"""
        with open(self.base_path_to_data_set, mode='a', newline='', encoding='utf-8') as dataset_file:
            dataset_writer = csv.writer(dataset_file)

            for data in rows_list:
                row = [
                    data.get("price", ""),
                    data.get("os", ""),
                    data.get("new", ""),
                    data.get("model_cpu", ""),
                    data.get("core", ""),
                    data.get("frequency_ghz", ""),
                    data.get("socket", ""),
                    data.get("ram_gb", ""),
                    data.get("ram_type", ""),
                    data.get("ram_ghz", ""),
                    data.get("model_gpu", ""),
                    data.get("vram_gb", ""),
                    data.get("storage_gb", ""),
                    data.get("mother_board", ""),
                    data.get("power_supply", ""),
                    data.get("estimation", ""),
                    data.get("link", "")
                ]
                dataset_writer.writerow(row)

price = '339 369 ₽'