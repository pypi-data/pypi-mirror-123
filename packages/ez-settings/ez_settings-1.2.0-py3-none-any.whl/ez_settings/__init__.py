import sys
if sys.version_info[0] < 3:
    from .ez_settings_py2 import EZSettingsPy2 as EZSettings
else:
    from .ez_settings_py3 import EZSettings
