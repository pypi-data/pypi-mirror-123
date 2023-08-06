from .ez_settings_base import EZSettingsBase
from .singleton import Singleton

class EZSettingsPy2(EZSettingsBase):
    __metaclass__ = Singleton
    def __init__(self, file_location=""):
        super(EZSettingsPy2, self).__init__(file_location=file_location)