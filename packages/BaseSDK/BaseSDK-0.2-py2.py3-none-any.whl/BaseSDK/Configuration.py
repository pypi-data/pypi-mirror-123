import hydra

from BaseSDK.Utils import Singleton


class Configuration(metaclass=Singleton):
    def __init__(self, context):
        if context == 'dev':
            self.url = 'http://192.168.0.111:31585/base-api'
            self.auth_url = 'http://192.168.0.111:31585/oauth2'
            self.endpoint = 'http://192.168.0.111:30197'
            self.task_url = 'http://192.168.0.111:31935'
            self.bucket = 'model-store'
