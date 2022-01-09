from .Functions import readJsonFile
from typing import Any
import json
import os


class Settings():
    def __init__(self,default_settings={}):
        self.default_settings = default_settings
        self.custom_settings = {}

    def get(self,key: str) -> Any:
        if key in self.custom_settings:
            return self.custom_settings[key]
        else:
            return self.default_settings[key]

    def set(self,key: str,value: Any):
        self.custom_settings[key] = value

    def save_to_file(self,path: str):
        if not os.path.isdir(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        with open(path,"w", encoding="utf-8") as f:
            json.dump(self.custom_settings,f,ensure_ascii=False,indent=4)

    def load_from_file(self,path: str):
        self.custom_settings = readJsonFile(path,{})
