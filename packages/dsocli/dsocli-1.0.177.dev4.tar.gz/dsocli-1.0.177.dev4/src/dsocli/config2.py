
import os
import re
from .constants import *
from .providers import KeyValueStoreProvider, Providers
from .logger import Logger
from .exceptions import DSOException
from .stages import Stages
from .appconfig import ContextSource


class ConfigProvider(KeyValueStoreProvider):
    def list(self, config, service, uninherited, filter):
        raise NotImplementedError()
    def set(self, config, key, value, service):
        raise NotImplementedError()
    def get(self, config, key, revision, service):
        raise NotImplementedError()
    def history(self, config, key, service):
        raise NotImplementedError()
    def unset(self, config, key, service):
        raise NotImplementedError()


class ConfigService2():

    def list(self, config, service='', uninherited=False, filter=None):
        self.config = config
        self.service = service
        provider = Providers.ConfigProvider(config)
        Logger.debug(f"Listing configurations: namespace={config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        response = provider.list(config,  service=service, uninherited=uninherited, filter=filter)
        return response


    def set(self, config, key, value, service=''):
        self.config = config
        self.service = service
        if not key: key = os.path.basename(filepath)
        # self.validate_key(key)
        provider = Providers.ConfigProvider(config)
        Logger.debug(f"Setting configuration '{key}': namespace={config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        return provider.set(config, key=key, value=value, service=service)


    def get(self, config, key, service=''):
        self.config = config
        self.service = service
        provider = Providers.ConfigProvider(config)
        Logger.debug(f"Getting configuration '{key}': namespace={config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        return provider.get(config, key=key, service=service)


    # def history(self, config, key):
    #     self.config = config
    #     provider = Providers.ConfigProvider(config)
    #     Logger.debug(f"Getting the history of configuration '{key}': namespace={config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
    #     return provider.history(config, service=service, key)


    def uset(self, config, key, service=''):
        self.config = config
        self.service = service
        provider = Providers.ConfigProvider(config)
        Logger.debug(f"Unsetting configuration '{key}': namespace={config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        return provider.unset(config, key=key, service=service)


Config2 = ConfigService2()