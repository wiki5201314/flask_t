from qiniu import Auth, put_file, etag
import qiniu.config


class Qiniu(object):
    QiniuUrl = "http://image.buroni.top/"

    def __init__(self):
        access_key = '8kUKQVJv2vBy3XrAiW8SHOAyoDzCKrdnfMv4xry9'
        secret_key = 'bk3FWj8qbvr-PY4AtcNi2X-pfHkVJCuWPyM24wYr'
        self.key = Auth(access_key, secret_key)
        self.bucket = "911w"

    def upload(self, path, filename):
        token = self.key.upload_token(self.bucket, filename, 3600)
        print("正在上传...")
        reform, inform = put_file(token, filename, path)
        if reform != None:
            print('已经成功地将{}->>{}'.format(filename, self.bucket))
            return 1
        else:
            print("上传失败")
            return 0