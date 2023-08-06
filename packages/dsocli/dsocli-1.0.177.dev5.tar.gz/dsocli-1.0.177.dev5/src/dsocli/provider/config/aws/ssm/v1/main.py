import boto3
from dsocli.exceptions import DSOException
from dsocli.logger import Logger
from dsocli.providers import Providers
from dsocli.config2 import ConfigProvider
from dsocli.stages import Stages
from dsocli.constants import *
from dsocli.dict_utils import set_dict_value
from dsocli.contexts import Contexts
from dsocli.aws_ssm_utils import *


__default_spec = {
    'pathPrefix': '/dso/v1/config',
}

def get_default_spec():
    return __default_spec.copy()


class AwsSsmConfigProvider(ConfigProvider):

    def __init__(self):
        super().__init__('config/aws/ssm/v1')


    ### adds service name to the artifactStore prefix
    def get_path_prefix(self, service):
        configPathPrefix = self.config.config_spec('pathPrefix')
        if not configPathPrefix.endswith('/'): configPathPrefix += '/'
        return configPathPrefix + service


    def list(self, config, service, uninherited=False, filter=None):
        self.config = config
        self.service = service
        Logger.debug(f"Listing SSM configuration: namesape={config.namespace}, project={config.project}, application={config.application}, stage={config.stage}")
        configuration = load_context_ssm_configuration(config=config, parameter_type='String', path_prefix=self.get_path_prefix(service), uninherited=uninherited, filter=filter)
        result = {'Parameters': []}
        for key, details in configuration.items():
            item = {
                'Key': key,
                'RevisionId': str(details['Version']),
            }
            item.update(details)
            result['Parameters'].append(item)

        return result


    def set(self, config, key, value, service):
        self.config = config
        self.service = service
        Logger.debug(f"Checking SSM configuration overwrites '{key}': namesape={config.namespace}, project={config.project}, application={config.application}, stage={config.stage}")
        assert_ssm_parameter_no_namespace_overwrites(config=config, key=key, path_prefix=self.get_path_prefix(service))
        Logger.debug(f"Locating SSM configuration '{key}': namesape={config.namespace}, project={config.project}, application={config.application}, stage={config.stage}")
        found = locate_ssm_parameter_in_context_hierachy(config=config, key=key, path_prefix=self.get_path_prefix(service), uninherited=True)
        if found and not found['Type'] == 'String':
            raise DSOException(f"Failed to add parameter '{key}' becasue becasue the key is not available in the given context: namespace:{config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        path = get_ssm_path(context=config.context, key=key, path_prefix=self.get_path_prefix(service))
        Logger.debug(f"Adding SSM configuration: path={path}")
        response = add_ssm_paramater(path, value)
        result = {
                'RevisionId': str(response['Version']),
                'Key': key, 
                'Value': value,
                'Stage': config.short_stage,
                'Scope': config.context.scope_translation,
                'Origin': {
                    'Namespace': config.namespace,
                    'Project': config.project,
                    'Application': config.application,
                    'Stage': config.stage,
                },
                'Path': path,
            }
        result.update(response)
        return result



    def get(self, config, key, service, revision=None):
        self.config = config
        self.service = service
        Logger.debug(f"Locating SSM configuration '{key}': namesape={config.namespace}, project={config.project}, application={config.application}, stage={config.stage}")
        found = locate_ssm_parameter_in_context_hierachy(config=config, key=key, path_prefix=self.get_path_prefix(service))
        if not found:
            raise DSOException(f"Config '{key}' not found nor inherited in the given context: namespace:{config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        else:
            if not found['Type'] == 'String':
                raise DSOException(f"Config '{key}' not found in the given context: namespace:{config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        Logger.debug(f"Getting SSM configuration: path={found['Name']}")
        response = get_ssm_parameter_history(found['Name'])
        configuration = sorted(response['Parameters'], key=lambda x: int(x['Version']), reverse=True)
        if revision is None:
            ### get the latest revision
            result = {
                    'RevisionId': str(configuration[0]['Version']),
                    'Date': configuration[0]['LastModifiedDate'].strftime('%Y/%m/%d-%H:%M:%S'),
                    'Key': key, 
                    'Value': configuration[0]['Value'],
                    'Scope': found['Scope'],
                    'Origin': found['Origin'],
                    'Path': found['Name'],
                    'User': configuration[0]['LastModifiedUser'],
                    }
                
        else:
            ### get specific revision
            configuration = [x for x in configuration if str(x['Version']) == revision]
            if not configuration:
                raise DSOException(f"Revision '{revision}' not found for parameter '{key}' in the given context: namespace:{config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
            result = {
                    'RevisionId':str(configuration[0]['Version']),
                    'Date': configuration[0]['LastModifiedDate'].strftime('%Y/%m/%d-%H:%M:%S'),
                    'Key': key, 
                    'Value': configuration[0]['Value'],
                    'Scope': found['Scope'],
                    'Origin': found['Origin'],
                    'Path': found['Name'],
                    'User': configuration[0]['LastModifiedUser'],
                    }

        return result


    def history(self, config, key, service):
        self.config = config
        self.service = service
        Logger.debug(f"Locating SSM configuration '{key}': namesape={config.namespace}, project={config.project}, application={config.application}, stage={config.stage}")
        found = locate_ssm_parameter_in_context_hierachy(config=config, key=key, path_prefix=self.get_path_prefix(service))
        if not found:
            raise DSOException(f"Config '{key}' not found in the given context: namespace:{config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        else:
            if not found['Type'] == 'String':
                raise DSOException(f"Config '{key}' not found in the given context: namespace:{config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        Logger.debug(f"Getting SSM configuration: path={found['Name']}")
        response = get_ssm_parameter_history(found['Name'])
        configuration = sorted(response['Parameters'], key=lambda x: int(x['Version']), reverse=True)
        result = { "Revisions":
            [{
                'RevisionId': str(parameter['Version']),
                'Date': parameter['LastModifiedDate'].strftime('%Y/%m/%d-%H:%M:%S'),
                'Key': key,
                'Value': parameter['Value'],
                # 'Scope': found['Scope'],
                # 'Origin': found['Origin'],
                'User': parameter['LastModifiedUser'],
                # 'Path': found['Name'],
            } for parameter in configuration]
        }

        return result



    def unset(self, config, key, service):
        self.config = config
        self.service = service
        Logger.debug(f"Locating SSM configuration '{key}': namesape={config.namespace}, project={config.project}, application={config.application}, stage={config.stage}")
        ### only configuration owned by the context can be deleted, hence uninherited=True
        found = locate_ssm_parameter_in_context_hierachy(config=config, key=key, path_prefix=self.get_path_prefix(service), uninherited=True)
        if not found:
            raise DSOException(f"Config '{key}' not found in the given context: namespace:{config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        else:
            # if len(found) > 1:
            #     Logger.warn(f"More than one parameter found at '{found['Name']}'. The first one taken, and the rest were discarded.")
            if not found['Type'] == 'String':
                raise DSOException(f"Config '{key}' not found in the given context: namespace:{config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        Logger.debug(f"Deleting SSM configuration: path={found['Name']}")
        delete_ssm_parameter(found['Name'])
        result = {
                'Key': key,
                'Stage': found['Stage'],
                'Scope': found['Scope'],
                'Origin': found['Origin'],
                'Path': found['Name'],
                }
        return result


def register():
    Providers.register(AwsSsmConfigProvider())
