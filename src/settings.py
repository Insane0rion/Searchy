class Settings:
    @staticmethod
    def load_settings(path_to_settings) -> dict:
        with open(path_to_settings, 'r') as f:
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

#TODO insert write_settings method better
'''
    def write_settings(a):
		with open("test", 'w') as f:	
			for cat, options in b.items():
				f.write(f"[{cat}]\n\n")
				for option, value in options.items():
					f.write(f"{option} = '{value}'\n")
				f.write("\n\n")
    '''
    