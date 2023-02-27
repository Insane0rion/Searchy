from os import path
from pathlib import Path
from src.settings import Settings

class FileHandler:
    def __init__(self):
        self.root = self._setRoot
        self.settings_file = Path(self.root + 'settings.ini')

    @property
    def _setRoot(self):
        splitted_path = path.realpath(__file__).split("/")
        for _ in range(2):
            del splitted_path[-1]
        return "/".join(splitted_path) + "/"

    def getSettings(self) -> dict | bool:
        if prove_settings_file:
            return self.load_settings()
        else:
            if self.create_settings():
                return self.load_settings()
            else:
                return False

    def prove_settings_file(self) -> bool:
        if self.settings_file.exists():
            return True
        print("Settings.ini does not exists creating settings.ini...")
        try:
            with open(self.settings_file, "w") as f:
                f.writelines(
                "[Generell Settings]\n# Currently supported languages: de\nLAN = 'de'\nSTANDART_AMT = '20'\nSTANDART_ENGINE = 'duck'\n######################\n[Youtube Settings]\n# Key needed to use the yt engine (Read Docs for more Info)\nAPI_KEY = ''\n######################\n# If you got any questions please\n# don't hesitate hit to an issue or\n# write me on github!"
                )
            print("Settings.ini has been created! If you want to use the Youtube engine please insert you're API-Key")
            return True
        except:
            return False

    def load_settings(self) -> dict:
        with open(self.settings_file, 'r') as f:
            splitted_text = f.readlines()
        raw_settings = () # Tuple to store raw settings lines
        for line in splitted_text:
            if line.startswith(('#','[')): # Checking if its necessary
                pass
            else:
                raw_settings = (*raw_settings, line)
        settings = {}
        for setting in raw_settings:
            setting=setting.split("\n")[0]
            key = setting.split(" ")[0]
            value= setting.split("'")[1]
            settings[key] = value
        return settings

    def create_settings(self) -> bool:
        settings = {"General Settings": {"LAN":'de',
                                         "STANDARD_ENGINE":'duck',
                                         'STANDARD_AMT':'20'},
                    "Youtube Settings": {"API_KEY":''}}
        try:
            with open(self.settings_file, 'w') as f:
                for cat, options in settings.items():
                    f.write(f"[{cat}]\n\n")
                    for option, value in options.items():
                        f.write(f"{option} = '{value}'\n")
                    f.write("\n\n")
            return True
        except:
            print("Error creating settings.ini file...\nRunning with standard parameters but issue an ticket on"
                  " github if this keeps happening!")
            return False
