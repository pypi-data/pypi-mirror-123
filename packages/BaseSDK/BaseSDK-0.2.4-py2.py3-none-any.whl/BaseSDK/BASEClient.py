import requests
import logging
import os

from BaseSDK import Utils
from BaseSDK.Configuration import *
from BaseSDK.ClientException import ResourceException, AuthException

from multiprocessing import Pool

import json

url_dict = {
    'get_dataset': '/sdk/datasets/{dataset_id}/files',
    'get_labels': '/sdk/labels',
    'get_categories': '/datasets/{dataset_id}/categories',
    'get_model_upload_url': '/sdk/models/{model_name}/upload',
    'get_pretrain': '/model-store/pretrain-models/{model_name}',
    'get_model': '/sdk/models',
    'get_status':'/tasks/{task_id}',
    'get_callback_upload_model':'/sdk/models/upload',
    'get_callback_training': '/tasks/{task_id}/callback',
    'get_callback_serving': '/tasks/{task_id}/callback',
}


class BASEClient(metaclass=Singleton):
    def __init__(self, apiKey=None, context='prod'):
        self.logger = logging.getLogger('BASEClient')
        self.config = Configuration(context)
        self.apiKey = apiKey



    def get_dataset_files(self, dataset_id, batch='batch-0', sensor='all'):
        """

        Args:
            dataset_id: id of the dataset to download
            batch: the batch name of the dataset, the default is 'batch-0'
            sensor: the sensor type of the files to download, the default is 'all'

        Returns:
            files: file list
        """
        payload = {
            'batch': batch,
            'sensor': sensor
        }
        url = self.config.url + url_dict.get('get_dataset').format(dataset_id=dataset_id)
        try:
            dataset_resp = requests.get(url=url,
                                        params=payload,
                                        headers={'apiKey': self.apiKey})

            if dataset_resp.status_code == 200:
                content = dataset_resp.json()
                if content['code'] == 200:
                    return content['data']
                else:
                    raise ResourceException(content['msg'])
            else:
                raise AuthException(dataset_resp.reason)
        except Exception as e:
            raise e

    def download_dataset(self, dataset_id, save_path, batch='batch-0', sensor='all'):
        """

        Args:
            dataset_id: id of the dataset to download
            save_path: local path to save the files
            batch: the batch name of the dataset, the default is 'batch-0'
            sensor: the sensor type of the files to download, the default is 'all'

        Returns:
            True if the dataset files downloaded successfully.
        """
        Utils.makedir(save_path)
        sensors = self.get_dataset_files(dataset_id, batch, sensor)
        if not sensors:
            self.logger.error("No sensors found in the dataset.")
            return False

        for sensor, files in sensors.items():

            data = [[os.path.join(save_path, _file['filename']), _file['url']] for _file in files]
            with Pool(5) as pool:
                pool.map(Utils.download_binary, data)

        return True

    def download_labels(self, dataset_id, save_path, batch='batch-0', sensor='all', ):
        """

        Args:
            dataset_id: id of the dataset to download
            save_path: local path to save the files
            batch: the batch name of the dataset, the default is 'batch-0'
            sensor: the sensor type of the files to download, the default is 'all'

        Returns:
             True if the dataset files downloaded successfully.
        """
        Utils.makedir(save_path)
        label_url = self.config.url + url_dict.get('get_labels')
        payload = {
            'datasetId':dataset_id,
            'batch': batch,
            'sensor': sensor
        }
        try:
            labels_resp = requests.get(url=label_url,
                                        params=payload,
                                        headers={'apiKey': self.apiKey})
            if labels_resp.status_code == 200:
                content = labels_resp.json()
                if content['code'] == 200:
                    labels = content['data']
                    for sensor, label in labels.items():
                        file_name = os.path.join(save_path, dataset_id+'-'+sensor+'.json')
                        with open(file_name, 'w') as handle:
                            json.dump(label,handle)
                    return True
                else:
                    raise ResourceException(content['msg'])
            else:
                raise AuthException(labels_resp.reason)

        except Exception as e:
            raise e

    def get_categories(self, dataset_id, feature_type):
        """
        Args:
            dataset_id: id of the dataset that the
            feature_type:

        Returns:

        """
        try:
            payload = {
                'feature_type': feature_type,
            }
            category_resp = requests.get(
                url=self.config.url + url_dict.get('get_categories').format(dataset_id=dataset_id),
                params=payload,
                headers={'apiKey': self.apiKey}).json()
            if category_resp.status_code == 200 and category_resp['code'] == 200:
                _categories = category_resp['data']['categories']
                return [cate['name'] for cate in _categories]
        except Exception as e:
            raise e

    def upload_model(self, task_id, model_name, model_file):
        """

        Args:
            task_id: unique id of the task
            model_name: model unique name
            model_file: file path of the serializers model to upload

        Returns:
            True if upload successfully.
        """

        try:
            paylod = {
                "taskId":task_id
            }
            upload_resp = requests.get(url=self.config.url + url_dict.get('get_model_upload_url').format(model_name=model_name),
                                       params=paylod,
                                       headers={'apiKey': self.apiKey}).json()

            if upload_resp['code'] != 200:
                self.logger.warning(upload_resp['msg'])
                return

            url = upload_resp['data']['key']

            with open(model_file, 'rb') as file_to_upload:
                files = {'file': (model_file, file_to_upload)}
                upload_response = requests.put(url=url, files=files)

            self.logger.info(upload_response)

            return True

        except Exception as e:
            raise e

    def download_pretrain(self, model_name, save_path):
        """
        Args:
            model_name: model unique name
            save_path: local path to save the files

        Returns:
            True if download successfully.
        """
        try:
            Utils.makedir(save_path)
            # url = self.config.endpoint + url_dict.get("get_pretrain").format(model_name=model_name)
            url = 'http://192.168.0.111:30197/model-store/pretrain-models/ddrnet.pth?Content-Disposition=attachment%3B%20filename%3D%22pretrain-models%2Fddrnet.pth%22&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=boden%2F20210930%2F%2Fs3%2Faws4_request&X-Amz-Date=20210930T060339Z&X-Amz-Expires=432000&X-Amz-SignedHeaders=host&X-Amz-Signature=db216f6792d90a3377135a85130f385baa2f4e6ce1f070b58439ee6c0c081292'
            # payload = {"model_name": model_name}
            # header = {'apiKey': self.apiKey}
            # pretrain_resp = requests.get(url, params=payload, headers=header).json()
            pretrain_resp = requests.get(url)
            # if pretrain_resp['code'] != 200:
            #     self.logger.warning(pretrain_resp['msg'])
            #     return
            # data = (os.path.join(save_path, "{}.pth".format(model_name)), pretrain_resp['url'])
            data = (os.path.join(save_path, "{}.pth".format(model_name)), url)
            Utils.download_binary(data)
            return True

        except Exception as e:
            raise e

    def get_model(self, task_id):
        """
        Args:
            task_id: the unique id of the task

        Returns:
            model information.
        """
        try:
            payload = {"taskId": task_id}
            header = {'apiKey': self.apiKey}
            model_resp = requests.get(url=self.config.url + url_dict.get("get_model"), params=payload,
                                      headers=header).json()
            if model_resp['code'] != 200:
                self.logger.warning(model_resp['msg'])
                raise ResourceException(model_resp['msg'])

            return model_resp['data']

        except Exception as e:
            raise e


    def download_model(self, task_id, save_path):
        """
        Args:
            task_id: the unique id of the task
            model_name: model unique name
            save_path: local path to save the files

        Returns:
            True if download successfully.
        """
        try:
            Utils.makedir(save_path)
            model_resp = self.get_model(task_id)
            model_name = model_resp['modelName']
            url = model_resp['modelUrl']
            data = (os.path.join(save_path, "{}.pth".format(model_name)), url)
            Utils.download_binary(data)
            return True
        except Exception as e:
            raise e

    def get_status(self,task_id):
        try:
            _url = self.config.task_url + url_dict.get("get_status").format(task_id=task_id)
            resp = requests.get(_url,headers={'apiKey': self.apiKey}).json()
            # if resp['code'] != 200:
            #     self.logger.warning(resp['msg'])
            #     return
            print(resp)
            return True
        except Exception as e:
            raise e

    def callback_training(self, task_id):
        try:
            _url = self.config.task_url + url_dict.get("get_callback_training").format(task_id=task_id)
            msg = "training finished"
            resp = requests.post(_url,headers={'apiKey': self.apiKey}).json()
            # if resp['code'] != 200:
            #     self.logger.warning(resp['msg'])
            #     return
            print(resp)
            return True
        except Exception as e:
            raise e

    def callback_serving(self, task_id):
        try:
            _url = url_dict.get("get_callback_serving")
            msg = "Serving started"
            payload = {"msg": msg, "status": 1, "task_id": task_id}
            resp = requests.get(_url, params=payload, headers={'apiKey': self.apiKey}).json()
            if resp['code'] != 200:
                self.logger.warning(resp['msg'])
                return
            return True
        except Exception as e:
            raise e

    def callback_upload_model(self, task_id, upload_success=False):
        try:
            if upload_success:
                payload = {
                    'taskId':task_id,
                    'status':1
                }
            else:
                payload = {
                    "taskId":task_id,
                    "status":0
                }
            payload = json.dumps(payload)
            resp = requests.post(url=self.config.url + url_dict.get('get_callback_upload_model'),
                                 data=payload, headers={'apiKey': self.apiKey,'Content-Type':'application/json'}).json()
            if resp['code'] != 200:
                self.logger.warning(resp['msg'])
                return

            self.logger.info(resp['code'])
            return True
        except Exception as e:
            raise e

if __name__ == '__main__':

    token = ""
    dataset_id = ""
    c = BASEClient(token, "dev")  # "prod"

