class Config:
    def __init__(self, init_config:dict = {}):
        self._config = {}
        if len(init_config) > 0:
            self._config.update(init_config)

    @property
    def dict(self):
        return self._config

    def get(self, attribute:str, default=None):
        return self._config.get(attribute, default)

    def set(self, attribute:str, new_value):
        if attribute is not None:
            self._config[attribute] = new_value

    def update(self, updated_configs:dict):
        if updated_configs != None:
            for key, value in updated_configs.items():
                self._config[key] = value

    def copy(self, attribute:str, from_config, default):
        self.set(attribute, from_config.get(attribute, default))

# ----------------------------------------

if __name__ == '__main__':
    game = Config()
    print("Done")
