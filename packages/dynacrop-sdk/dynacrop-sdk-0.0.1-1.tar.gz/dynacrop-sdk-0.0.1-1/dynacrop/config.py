import json
import os

# TODO suggestion: move variable api_key to Config class
API_KEY: str = 'api_key'

CONFIG_PATH: str = os.path.join('sdk', 'config.json')


# TODO suggestion: implement as a singleton
class Config:
    """Authentication helper."""
    def __init__(self):
        """Constructs Config object."""
        try:
            with open(CONFIG_PATH) as configRead:
                self._config = json.load(configRead)
        except FileNotFoundError:
            raise

    @property
    def api_key(self) -> str:
        """API key property of the Config object.

        Returns:
            str: API key.
        """
        return self._config['api_key']

    @api_key.setter
    def api_key(self, api_key: str):
        """API key property setter.

        Args:
            api_key (str): API key.
        """
        self._config['api_key'] = api_key

    def save(self):
        """Saves configuration to the JSON config file."""
        with open(CONFIG_PATH, 'w') as configWrite:
            json.dump(self._config, configWrite)

    def __str__(self) -> str:
        """Returns structured configuration information."""
        return str(self._config)
