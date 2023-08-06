
import os
import re
from .constants import *
from .providers import ProviderBase, Providers
from .artifacts import ArtifactStore
from .logger import Logger
from .exceptions import DSOException
from .stages import Stages
from .appconfig import ContextSource


key_regex_pattern = r"^[a-zA-Z]([./a-zA-Z0-9_-]*[a-zA-Z0-9])?$"

class PackageProvider(ProviderBase):
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


class PackageService():
    

    service_name = 'package'


    # def validate_key(self, key):
    #     Logger.info(f"Validating package key '{key}'...")
    #     if not key:
    #         raise DSOException(MESSAGES['KeyNull'])
    #     if key == 'dso' or key.startswith('dso.'):
    #         raise DSOException(MESSAGES['DSOReserverdKey'].format(key))
    #     if not re.match(key_regex_pattern, key):
    #         raise DSOException(MESSAGES['InvalidKeyPattern'].format(key, key_regex_pattern))
    #     ### the regex does not check adjacent special chars
    #     if '..' in key:
    #         raise DSOException(MESSAGES['InvalidKeyStr'].format(key, '..'))

    #     if '//' in key:
    #         raise DSOException(MESSAGES['InvalidKeyStr'].format(key, '//'))


    @property
    def version_major(self):
        try:
            provider = Providers.ConfigProvider(self.config)
            return int(provider.get(self.config, key='version.major', service=self.service_name)['Value'])
        except DSOException:
            init_version_major = 0
            self.version_major = init_version_major
            return init_version_major

    @version_major.setter
    def version_major(self, value):
        Providers.ConfigProvider(self.config).set(self.config, key='version.major', value=str(value), service=self.service_name)


    @property
    def version_minor(self):
        try:
            provider = Providers.ConfigProvider(self.config)
            return int(provider.get(self.config, key='version.minor', service=self.service_name)['Value'])
        except DSOException:
            init_version_minor = 0
            self.version_minor = init_version_minor
            return init_version_minor

    @version_minor.setter
    def version_minor(self, value):
        provider = Providers.ConfigProvider(self.config)
        provider.set(self.config, key='version.minor', value=str(value), service=self.service_name)


    @property
    def version_patch(self):
        try:
            provider = Providers.ConfigProvider(self.config)
            return int(provider.get(self.config, key='version.patch', service=self.service_name)['Value'])
        except DSOException:
            init_version_patch = 0
            self.version_patch = init_version_patch
            return init_version_patch

    @version_patch.setter
    def version_patch(self, value):
        provider = Providers.ConfigProvider(self.config)
        provider.set(self.config, key='version.patch', value=str(value), service=self.service_name)


    @property
    def version_build(self):
        try:
            provider = Providers.ConfigProvider(self.config)
            return int(provider.get(self.config, key='version.build', service=self.service_name)['Value'])
        except DSOException:
            init_version_build = 0
            self.version_build = init_version_build
            return init_version_build


    @version_build.setter
    def version_build(self, value):
        provider = Providers.ConfigProvider(self.config)
        provider.set(self.config, key='version.build', value=str(value), service=self.service_name)


    def list(self, config, filter=None):
        self.config = config
        provider = Providers.PackageProvider(config)
        Logger.info(f"Listing packages: namespace={config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        response = ArtifactStore.list(config=config, service=self.service_name, filter=filter)
        result = {'Packages': response['Artifacts']}
        return result


    def build(self, config):
        self.config = config
        provider = Providers.PackageProvider(config)
        Logger.info(f"Building package: namespace={config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        artifact = provider.build(config)
        major = self.version_major
        minor = self.version_minor
        patch = self.version_patch
        build = self.version_build
        artifactKey = f"{major}.{minor}.{patch}.{build}"
        self.version_build = build + 1
        Logger.info(f"Adding package '{artifactKey}' to artifact store...")
        # changed = Logger.decrease_verbosity()
        # try:
        #     response = ArtifactStore.add(config=config, filepath=artifact, key=artifactKey ,service=self.service_name)
        # finally:
        #     if changed: Logger.increase_verbosity()
        response = ArtifactStore.add(config=config, filepath=artifact, key=artifactKey ,service=self.service_name)
        return response


    def get(self, config, key):
        self.config = config
        Logger.info(f"Getting package '{key}': namespace={config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        response = ArtifactStore.get(config=config, key=key, service=self.service_name)
        return response


    # def history(self, config, key):
    #     self.config = config
    #     provider = Providers.PackageProvider(config)
    #     Logger.info(f"Getting the history of package '{key}': namespace={config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
    #     return provider.history(config, key)


    def delete(self, config, key):
        self.config = config
        Logger.info(f"Deleting package '{key}': namespace={config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        response = ArtifactStore.delete(config=config, key=key, service=self.service_name)
        return response


Packages = PackageService()