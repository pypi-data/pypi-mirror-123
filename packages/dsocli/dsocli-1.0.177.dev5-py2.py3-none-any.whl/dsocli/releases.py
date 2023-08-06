
import os
import re
from .constants import *
from .providers import ProviderBase, Providers
from .artifacts import ArtifactStore
from .logger import Logger
from .exceptions import DSOException
from .stages import Stages
from .appconfig import AppConfig, ContextSource


key_regex_pattern = r"^[a-zA-Z]([./a-zA-Z0-9_-]*[a-zA-Z0-9])?$"

class ReleaseProvider(ProviderBase):
    def list(self, filter=None):
        raise NotImplementedError()
    def build(self, key):
        raise NotImplementedError()
    def get(self, key, revision=None):
        raise NotImplementedError()
    # def history(self, key):
    #     raise NotImplementedError()
    def delete(self, key):
        raise NotImplementedError()


class ReleaseService():
    
    @property
    def default_render_path(self):
        return AppConfig.working_dir


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


    def list(self, filter=None):
        provider = Providers.ReleaseProvider()
        Logger.info(f"Listing releases: namespace={AppConfig.namespace}, project={AppConfig.project}, application={AppConfig.application}, stage={AppConfig.short_stage}")
        response = ArtifactStore.list(path_prefix=self.PATH_PREFIX, filter=filter)
        result = {'Releases': response['Artifacts']}
        return result


    def create(self):
        provider = Providers.ReleaseProvider()
        Logger.info(f"Creating release: namespace={AppConfig.namespace}, project={AppConfig.project}, application={AppConfig.application}, stage={AppConfig.short_stage}")
        artifact = provider.create()
        Logger.info(f"Adding release to the release store...")
        response = ArtifactStore.add(filepath=artifact, path_prefix=self.PATH_PREFIX)
        return response


    def get(self, key):
        Logger.info(f"Getting release '{key}': namespace={AppConfig.namespace}, project={AppConfig.project}, application={AppConfig.application}, stage={AppConfig.short_stage}")
        response = ArtifactStore.get(key=key, path_prefix=self.PATH_PREFIX)
        return response


    # def history(self, key):
    #     self.config = config
    #     provider = Providers.ReleaseProvider()
    #     Logger.info(f"Getting the history of release '{key}': namespace={AppConfig.namespace}, project={AppConfig.project}, application={AppConfig.application}, stage={AppConfig.short_stage}")
    #     return provider.history(config, key)


    def delete(self, key):
        Logger.info(f"Deleting release '{key}': namespace={AppConfig.namespace}, project={AppConfig.project}, application={AppConfig.application}, stage={AppConfig.short_stage}")
        response = ArtifactStore.delete(key=key, path_prefix=self.PATH_PREFIX)
        return response


Releases = ReleaseService()