from boto3.session import Session
import logging
import os

class S3Client(object):
    def __init__(self, **kwarg):
        self.logger = logging.getLogger('S3Client')

        self.ak = kwarg.get('ak')
        self.sk = kwarg.get('sk')
        self.endpoint = kwarg.get('endpoint')
        self.bucket = kwarg.get('bucket')

        try:
            self.session = Session(self.ak, self.sk)
            self.client = self.session.client('s3', endpoint_url=self.endpoint)
        except Exception as e:
            self.logger.warning(e)
            raise e

    def download_images(self, prefix_path: dict, local_path: str):
        if prefix_path and local_path:
            for sensor, path in prefix_path.items():
                file_list = self.client.list_objects(Bucket=self.bucket,
                                                     Prefix=self.__fix_prefix(path),
                                                     Delimiter='/')['Contents']
                self.logger.info('Download {} files from {}...'.format(len(file_list), path))

                for file_object in file_list:
                    if not os.path.exists(os.path.join(local_path, sensor)):
                        os.makedirs(os.path.join(local_path, sensor))
                    filepath = os.path.join(local_path, sensor, self.__get_filename(file_object))
                    self.__download(file_object['Key'], filepath)
            return True
        return False

    def __download(self, key, filepath):
        try:
            obj = self.client.get_object(self.bucket, Key=key)
            with open(filepath, 'wb') as f:
                f.write(obj['Body'].read())
        except Exception as e:
            raise e

    @staticmethod
    def __get_filename(obj):
        return obj.split('/')[-1]

    @staticmethod
    def __fix_prefix(prefix: str):
        if prefix.endswith('/'):
            return prefix
        else:
            return prefix+'/'


if __name__ == '__main__':
    s3 = S3Client(ak='boden',sk='bodenai2019', endpoint='http://192.168.0.111:30467', bucket='base-test')
    # res = s3.client.list_objects(Bucket=s3.bucket, Prefix='3D资源/', Delimiter='/')
    # s3.client.generate_presigned_url()
    # print(len(res['Contents']))
    # print(res['Contents'][0]['Key'].split('/')[-1])
    # url = s3.client.generate_presigned_url(ClientMethod='put_object',
    #                                        Fields={'file'},
    #                                  Params={'Bucket': 'model-store','Key':'/1111/1111.pth'},
    #                                  ExpiresIn=3600,
    #                                  HttpMethod='PUT')
    upload_details = s3.client.generate_presigned_post('model-store', '/111/111.pth')
    print(upload_details)
    import requests

    filename_to_upload = './Utils.py'

    with open(filename_to_upload, 'rb') as file_to_upload:
        files = {'file': (filename_to_upload, file_to_upload)}
        upload_response = requests.post(upload_details['url'], data=upload_details['fields'], files=files)

    print(f"Upload response: {upload_response.status_code}")