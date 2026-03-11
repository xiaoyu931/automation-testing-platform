import yaml
import os


class Settings:

    def __init__(self, env):
        self.env = env
        self.config = self._load_config()
        self.project_root = os.path.dirname(os.path.dirname(__file__))

    def _load_config(self):
        base_dir = os.path.dirname(__file__)
        file_path = os.path.join(base_dir, f"{self.env}.yaml")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Config file not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    @property
    def base_url(self):
        return self.config.get("base_url")

    @property
    def timeout(self):
        return self.config.get("timeout")

    @property
    def default_browser(self):
        return self.config.get("browser")

    @property
    def get_success_threshold(self):
        # 80 是默认值
        return self.config.get("success_threshold", 80)

    @property
    def get_data_dir(self):
        return os.path.join(self.project_root, "data", self.env)
