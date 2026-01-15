import csv
import math

import numpy as np
from sklearn.impute import SimpleImputer
import pandas as pd


class ConstructionCSV:
    def __init__(self, base_path_to_data_set):
        self.base_path_to_data_set = base_path_to_data_set

    def create_csv(self):
        """Создаёт CSV файл с заголовками"""
        try:
            with open(self.base_path_to_data_set, mode='w', encoding='utf-8') as dataset_file:
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
                print(f"{self.base_path_to_data_set} успешно создан!")

        except Exception as e:
            print(f"Ошибка при создании файла: {e}")

    def open_csv(self):
        try:
            with open(self.base_path_to_data_set, mode='r', newline='', encoding='utf-8') as dataset_file:
                return list(csv.reader(dataset_file))

        except Exception as e:
            return f"Ошика при открытии файла: {e}"

    def add_row(self, data):
        """Добавляет одну строку в конец файла"""
        try:
            with open(self.base_path_to_data_set, mode='a', newline='', encoding='utf-8') as dataset_file:
                dataset_writer = csv.writer(dataset_file)
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
                print(f"В {self.base_path_to_data_set} успешно записана строка!")

        except Exception as e:
            print(f"Ошибка при записи строки: {e}")

    def add_rows(self, rows_list):
        """Добавляет несколько строк в конец файла"""
        try:
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
                    dataset_writer.writerows(row)
                    print(f"В {self.base_path_to_data_set} успешно записаны строки!")

        except Exception as e:
            print(f"Ошибка при записи строк: {e}")

    def merge_csv(self, slave_file_path):
        try:
            with open(slave_file_path, mode='r', newline='', encoding='utf-8') as slave_file:
                slave_file_list = list(csv.reader(slave_file))[1:]
                print(f"{slave_file_path} записан в список")
        except Exception as e:
            print(f"Ошибка: {e}")

        try:
            with open(self.base_path_to_data_set, mode='a', newline='', encoding='utf-8') as dataset_file:
                writer = csv.writer(dataset_file)
                writer.writerows(slave_file_list)
                print(f"Список записан в {self.base_path_to_data_set}")
        except Exception as e:
            print(f"Ошибка: {e}")

    def check_on_duplicate(self):
        df = pd.read_csv(self.base_path_to_data_set)

        duplicates_count = df.duplicated().sum()

        df_unique = df.drop_duplicates()
        df_unique.to_csv(self.base_path_to_data_set, index=False)

        print(f"✓ Удалено дубликатов: {duplicates_count}")

    def remove_nan(self):
        """Заполнить NaN значения в датасете"""
        df = pd.read_csv(self.base_path_to_data_set)

        nan_counts = df.isna().sum()
        if nan_counts.sum() > 0:
            print("Найдены NaN значения:")
            print(nan_counts[nan_counts > 0])

        numeric_cols = ['core', 'frequency_ghz', 'ram_gb', 'ram_ghz',
                        'vram_gb', 'storage_gb', 'power_supply', 'price']

        for col in numeric_cols:
            if col in df.columns:
                df[col].fillna(0.0, inplace=True)

        string_cols = ['os', 'new', 'model_cpu', 'socket', 'ram_type',
                       'model_gpu', 'mother_board']

        for col in string_cols:
            if col in df.columns:
                df[col].fillna("unknown", inplace=True)

        df.to_csv(self.base_path_to_data_set, index=False)
        print(f"✓ Очистка завершена. Обработано {len(df)} строк")