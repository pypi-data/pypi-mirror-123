from .ez_settings_base import EZSettingsBase
from .singleton import Singleton


class EZSettings(EZSettingsBase, metaclass=Singleton):
    def __init__(self, file_location=""):
        super().__init__(file_location=str(file_location))
