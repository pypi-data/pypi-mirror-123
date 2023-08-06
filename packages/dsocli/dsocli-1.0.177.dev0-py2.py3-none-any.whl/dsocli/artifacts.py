
import os
import re
from .constants import *
from .providers import Providers
from .logger import Logger
from .exceptions import DSOException
from .stages import Stages
from .config import ContextSource


class ArtifactStoreService():
    
    @property

    def list(self, config, filter=None, path_prefix=''):
        self.config = config
        provider = Providers.StorageProvider(config)
        Logger.detail(f"Listing artifacts: namespace={config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        response = provider.list(config, filter=filter, path_prefix=path_prefix)
        result = {
            'Artifacts': response['Files']
        }
        return result

    def add(self, config, filepath, key=None, path_prefix=''):
        self.config = config
        if not key: key = os.path.basename(filepath)
        # self.validate_key(key)
        provider = Providers.StorageProvider(config)
        Logger.detail(f"Adding artifact '{key}': namespace={config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        return provider.add(config, filepath=filepath, key=key, path_prefix=path_prefix)


    def get(self, config, key, path_prefix=''):
        self.config = config
        provider = Providers.StorageProvider(config)
        Logger.detail(f"Getting artifact '{key}': namespace={config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        return provider.get(config, key=key, path_prefix=path_prefix)


    # def history(self, config, key):
    #     self.config = config
    #     provider = Providers.StorageProvider(config)
    #     Logger.detail(f"Getting the history of artifact '{key}': namespace={config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
    #     return provider.history(config, key)


    def delete(self, config, key, path_prefix=''):
        self.config = config
        provider = Providers.StorageProvider(config)
        Logger.detail(f"Deleting artifact '{key}': namespace={config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        return provider.delete(config, key=key, path_prefix=path_prefix)



ArtifactStore = ArtifactStoreService()