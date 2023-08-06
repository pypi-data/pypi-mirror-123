
import os
import re
from .constants import *
from .providers import ProviderBase, Providers
from .artifacts import ArtifactStore
from .logger import Logger
from .exceptions import DSOException
from .stages import Stages
from .config import ContextSource


key_regex_pattern = r"^[a-zA-Z]([./a-zA-Z0-9_-]*[a-zA-Z0-9])?$"

class ReleaseProvider(ProviderBase):
    def list(self, config, filter=None):
        raise NotImplementedError()
    def build(self, config, key):
        raise NotImplementedError()
    def get(self, config, key, revision=None):
        raise NotImplementedError()
    # def history(self, config, key):
    #     raise NotImplementedError()
    def delete(self, config, key):
        raise NotImplementedError()


class ReleaseService():
    
    @property
    def default_render_path(self):
        return self.config.working_dir


    PATH_PREFIX = 'releases/'


    def validate_key(self, key):
        Logger.info(f"Validating release key '{key}'...")
        if not key:
            raise DSOException(MESSAGES['KeyNull'])
        if key == 'dso' or key.startswith('dso.'):
            raise DSOException(MESSAGES['DSOReserverdKey'].format(key))
        if not re.match(key_regex_pattern, key):
            raise DSOException(MESSAGES['InvalidKeyPattern'].format(key, key_regex_pattern))
        ### the regex does not check adjacent special chars
        if '..' in key:
            raise DSOException(MESSAGES['InvalidKeyStr'].format(key, '..'))

        if '//' in key:
            raise DSOException(MESSAGES['InvalidKeyStr'].format(key, '//'))


    def list(self, config, filter=None):
        self.config = config
        provider = Providers.ReleaseProvider(config)
        Logger.info(f"Listing releases: namespace={config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        response = ArtifactStore.list(config=config, path_prefix=self.PATH_PREFIX, filter=filter)
        result = {'Releases': response['Artifacts']}
        return result


    def create(self, config):
        self.config = config
        provider = Providers.ReleaseProvider(config)
        Logger.info(f"Creating release: namespace={config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        artifact = provider.create(config)
        Logger.info(f"Adding release to the release store...")
        response = ArtifactStore.add(config=config, filepath=artifact, path_prefix=self.PATH_PREFIX)
        return response


    def get(self, config, key):
        self.config = config
        Logger.info(f"Getting release '{key}': namespace={config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        response = ArtifactStore.get(config=config, key=key, path_prefix=self.PATH_PREFIX)
        return response


    # def history(self, config, key):
    #     self.config = config
    #     provider = Providers.ReleaseProvider(config)
    #     Logger.info(f"Getting the history of release '{key}': namespace={config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
    #     return provider.history(config, key)


    def delete(self, config, key):
        self.config = config
        Logger.info(f"Deleting release '{key}': namespace={config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        response = ArtifactStore.delete(config=config, key=key, path_prefix=self.PATH_PREFIX)
        return response


Releases = ReleaseService()