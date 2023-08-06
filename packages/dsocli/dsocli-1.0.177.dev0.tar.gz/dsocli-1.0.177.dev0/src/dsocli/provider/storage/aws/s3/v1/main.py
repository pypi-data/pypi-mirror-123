from dsocli.exceptions import DSOException
from dsocli.logger import Logger
from dsocli.providers import Providers, FileStoreProvider
from dsocli.stages import Stages
from dsocli.constants import *
from dsocli.contexts import Contexts
from dsocli.aws_s3_utils import *
from dsocli.settings import *


__default_spec = {
    'bucket': 'mybucket',
    'pathPrefix': 'dso/v1',
}


def get_default_spec():
    return __default_spec.copy()


class AwsS3FileStoreProvider(FileStoreProvider):

    def __init__(self):
        super().__init__('storage/aws/s3/v1')


    def get_bucket_name(self):
        return self.config.storage_spec('bucket')


    def get_path_prefix(self, extraPrefix=''):
        return self.config.storage_spec('pathPrefix') + extraPrefix


    def list(self, config, filter=None, path_prefix=''):
        self.config = config
        Logger.debug(f"Listing S3 objecs: namespace:{config.namespace}, project={config.project}, application={config.application}, stage={config.stage}")
        items = s3_context_list_files(config=config, bucket=self.get_bucket_name(), path_prefix=self.get_path_prefix(path_prefix), filter=filter)
        result = {'Files': items}
        return result


    def add(self, config, filepath, key, path_prefix=''):
        self.config = config
        Logger.debug(f"Adding S3 object '{key}': namespace:{config.namespace}, project={config.project}, application={config.application}, stage={config.stage}")
        response = s3_context_add_file(config, filepath=filepath, bucket=self.get_bucket_name(), key=key, path_prefix=self.get_path_prefix(path_prefix))
        result = {
                # 'RevisionId': str(response['Version']),
                'Key': key,
                'Context': {
                    'Namespace': config.namespace,
                    'Project': config.project,
                    'Application': config.application,
                    'Stage': config.stage,
                },
            }
        result.update(response)
        return result


    def get(self, config, key, revision=None, path_prefix=''):
        self.config = config
        Logger.debug(f"Getting S3 object '{key}': namespace:{config.namespace}, project={config.project}, application={config.application}, stage={config.stage}")
        response = s3_context_get_file(config, bucket=self.get_bucket_name(), key=key, path_prefix=self.get_path_prefix(path_prefix))
        if not response:
            raise DSOException(f"Object '{key}' not found in the given context: namespace:{config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        result = {
                # 'RevisionId': str(response['Version']),
                'Key': key,
                'Context': {
                    'Namespace': config.namespace,
                    'Project': config.project,
                    'Application': config.application,
                    'Stage': config.stage,
                },
            }
        result.update(response)
        return result

        # response = get_ssm_storage_history(found['Name'])
        # storage = sorted(response['Parameters'], key=lambda x: int(x['Version']), reverse=True)
        # if revision is None:
        #     ### get the latest revision
        #     result = {
        #             'RevisionId': str(storage[0]['Version']),
        #             'Date': storage[0]['LastModifiedDate'].strftime('%Y/%m/%d-%H:%M:%S'),
        #             'Key': key, 
        #             'Scope': found['Scope'],
        #             'Origin': found['Origin'],
        #             'User': storage[0]['LastModifiedUser'],
        #             'Path': found['Name'],
        #             'Contents': storage[0]['Value'],
        #             }
        # else:
        #     ### get specific revision
        #     storage = [x for x in storage if str(x['Version']) == revision]
        #     if not storage:
        #         raise DSOException(f"Revision '{revision}' not found for storage '{key}' in the given context: namespace:{config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        #     result = {
        #             'RevisionId': str(storage[0]['Version']),
        #             'Date': storage[0]['LastModifiedDate'].strftime('%Y/%m/%d-%H:%M:%S'),
        #             'Key': key, 
        #             'Scope': found['Scope'],
        #             'Origin': found['Origin'],
        #             'Path': found['Name'],
        #             'User': storage[0]['LastModifiedUser'],
        #             'Contents': storage[0]['Value'],
        #             }

        return result



    def history(self, config, key, include_contents=False):
        self.config = config
        Logger.debug(f"Locating S3 storage '{key}': namespace:{config.namespace}, project={config.project}, application={config.application}, stage={config.stage}")
        found = locate_ssm_parameter_in_context_hierachy(config=config, key=key, path_prefix=self.get_path_prefix())
        if not found:
            raise DSOException(f"Storage '{key}' not found in the given context: namespace:{config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        else:
            if not found['Type'] == 'StringList':
                raise DSOException(f"Storage '{key}' not found in the given context: namespace:{config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        Logger.debug(f"Getting S3 storage: path={found['Name']}")
        response = get_ssm_parameter_history(found['Name'])
        storage = sorted(response['Parameters'], key=lambda x: int(x['Version']), reverse=True)
        if include_contents:
            result = { "Revisions":
                [{
                    'RevisionId': str(storage['Version']),
                    'Date': storage['LastModifiedDate'].strftime('%Y/%m/%d-%H:%M:%S'),
                    'Key': key,
                    # 'Scope': found['Scope'],
                    # 'Origin': found['Origin'],
                    'User': storage['LastModifiedUser'],
                    # 'Path': found['Name'],
                    'Contents': storage[0]['Value'],

                } for storage in storage]
            }
        else:
            result = { "Revisions":
                [{
                    'RevisionId': str(storage['Version']),
                    'Date': storage['LastModifiedDate'].strftime('%Y/%m/%d-%H:%M:%S'),
                    'Key': key,
                    # 'Scope': found['Scope'],
                    # 'Origin': found['Origin'],
                    'User': storage['LastModifiedUser'],
                    # 'Path': found['Name'],
                } for storage in storage]
            }

        return result



    def delete(self, config, key, path_prefix=''):
        self.config = config
        Logger.debug(f"Deleting S3 object '{key}': namespace:{config.namespace}, project={config.project}, application={config.application}, stage={config.stage}")
        response = s3_context_delete_file(config, bucket=self.get_bucket_name(), key=key, path_prefix=self.get_path_prefix(path_prefix))
        if not response:
            raise DSOException(f"Object '{key}' not found in the given context: namespace:{config.namespace}, project={config.project}, application={config.application}, stage={config.short_stage}")
        result = {
                # 'RevisionId': str(response['Version']),
                'Key': key,
                'Context': {
                    'Namespace': config.namespace,
                    'Project': config.project,
                    'Application': config.application,
                    'Stage': config.stage,
                },
            }
        result.update(response)
        return result



def register():
    Providers.register(AwsS3FileStoreProvider())
