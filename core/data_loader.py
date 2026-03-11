import yaml
import os
from config.settings import Settings

class DataLoader:

    @staticmethod
    def load_yaml(file_name, key):
        base_path = os.path.dirname(os.path.dirname(__file__))
        file_path = os.path.join(base_path, "data", file_name)

        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        if key not in data:
            raise KeyError(f"{key} not found in {file_name}")

        return data[key]

    # def load_login_data(settings):
    #     data_dir = settings.data_dir
    #     file_path = f"data/{data_dir}/login_data.yaml"
    #     return DataLoader.load_yaml(file_path, "login_cases")