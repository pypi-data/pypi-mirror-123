
import os
import re
from .constants import *
from .providers import Providers
from .logger import Logger
from .exceptions import DSOException
from .stages import Stages
from .appconfig import ContextSource


class ArtifactStoreService():

    def list(self, config, service, filter=None):
        self.config = config
        provider = Providers.ArtifactStoreProvider(config)
        Logger.info(f"Listing artifacts: namespace={config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        response = provider.list(config, filter=filter, service=service)
        result = {
            'Artifacts': response['Files']
        }
        return result

    def add(self, config, filepath, service, key=None):
        self.config = config
        if not key: key = os.path.basename(filepath)
        # self.validate_key(key)
        provider = Providers.ArtifactStoreProvider(config)
        Logger.info(f"Adding artifact '{key}': namespace={config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        return provider.add(config, filepath=filepath, key=key, service=service)


    def get(self, config, key, service):
        self.config = config
        provider = Providers.ArtifactStoreProvider(config)
        Logger.info(f"Getting artifact '{key}': namespace={config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        return provider.get(config, key=key, service=service)


    # def history(self, config, key):
    #     self.config = config
    #     provider = Providers.ArtifactStoreProvider(config)
    #     Logger.info(f"Getting the history of artifact '{key}': namespace={config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
    #     return provider.history(config, key)


    def delete(self, config, key, service):
        self.config = config
        provider = Providers.ArtifactStoreProvider(config)
        Logger.info(f"Deleting artifact '{key}': namespace={config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        return provider.delete(config, key=key, service=service)



ArtifactStore = ArtifactStoreService()
