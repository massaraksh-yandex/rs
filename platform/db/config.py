from platform.db.settings import Settings
import json


class Config:
    def __init__(self, settings = Settings(), map = None):
        if map is None:
            with open(settings.CONFIG_FILE, 'r') as f:
                self.params = json.load(f)
        else:
            self.params = map
        self.settings = settings
        self.name = settings.CONFIG_FILE


    def __repr__(self):
        return json.dumps(self.params)

    def serialize(self):
        with open(self.settings.CONFIG_FILE, 'w') as f:
            json.dump(self.params, f, indent=4, sort_keys=True)