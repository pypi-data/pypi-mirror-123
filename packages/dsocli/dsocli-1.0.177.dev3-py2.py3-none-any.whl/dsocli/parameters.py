import re
from .logger import Logger
from .providers import KeyValueStoreProvider, Providers
from .stages import Stages
from .constants import *
from .exceptions import *
from .config import ContextSource


key_regex_pattern = r"^[a-zA-Z]([.a-zA-Z0-9_-]*[a-zA-Z0-9])?$"

class ParameterProvider(KeyValueStoreProvider):
    def list(self, config, uninherited=False, filter=None):
        raise NotImplementedError()
    def add(self, config, key, value):
        raise NotImplementedError()
    def get(self, config, key, revision=None):
        raise NotImplementedError()
    def history(self, config, key):
        raise NotImplementedError()
    def delete(self, config, key):
        raise NotImplementedError()


class ParameterService():

    def validate_key(self, key):
        Logger.info(f"Validating parameter key '{key}'...")
        if not key:
            raise DSOException(MESSAGES['KeyNull'])
        if key == 'dso' or key.startswith('dso.'):
            raise DSOException(MESSAGES['DSOReserverdKey'].format(key))
        if not re.match(key_regex_pattern, key):
            raise DSOException(MESSAGES['InvalidKeyPattern'].format(key, key_regex_pattern))
        if '..' in key:
            raise DSOException(MESSAGES['InvalidKeyStr'].format(key, '..'))
            
    def list(self, config, uninherited=False, filter=None):
        self.config = config
        provider = Providers.ParameterProvider(config)
        Logger.info(f"Listing parameters: namespace={config.get_namespace(ContextSource.Target)}, project={config.get_project(ContextSource.Target)}, application={config.get_application(ContextSource.Target)}, stage={config.get_stage(ContextSource.Target, short=True)}, scope={config.scope}")
        return provider.list(config, uninherited, filter)

    def add(self, config, key, value):
        self.config = config
        self.validate_key(key)
        provider = Providers.ParameterProvider(config)
        Logger.info(f"Adding parameter '{key}': namespace={config.get_namespace(ContextSource.Target)}, project={config.get_project(ContextSource.Target)}, application={config.get_application(ContextSource.Target)}, stage={config.get_stage(ContextSource.Target, short=True)}, scope={config.scope}")
        return provider.add(config, key, value)

    def get(self, config, key, revision=None):
        self.config = config
        # self.validate_key(key)
        provider = Providers.ParameterProvider(config)
        Logger.info(f"Getting parameter '{key}': namespace={config.get_namespace(ContextSource.Target)}, project={config.get_project(ContextSource.Target)}, application={config.get_application(ContextSource.Target)}, stage={config.get_stage(ContextSource.Target, short=True)}, scope={config.scope}")
        return provider.get(config, key, revision)

    def history(self, config, key):
        self.config = config
        # self.validate_key(key)
        provider = Providers.ParameterProvider(config)
        Logger.info(f"Getting the history of parameter '{key}': namespace={config.get_namespace(ContextSource.Target)}, project={config.get_project(ContextSource.Target)}, application={config.get_application(ContextSource.Target)}, stage={config.get_stage(ContextSource.Target, short=True)}, scope={config.scope}")
        return provider.history(config, key)

    def delete(self, config, key):
        self.config = config
        # self.validate_key(key)
        provider = Providers.ParameterProvider(config)
        Logger.info(f"Deleting parameter '{key}': namespace={config.get_namespace(ContextSource.Target)}, project={config.get_project(ContextSource.Target)}, application={config.get_application(ContextSource.Target)}, stage={config.get_stage(ContextSource.Target, short=True)}, scope={config.scope}")
        return provider.delete(config, key)

Parameters = ParameterService()