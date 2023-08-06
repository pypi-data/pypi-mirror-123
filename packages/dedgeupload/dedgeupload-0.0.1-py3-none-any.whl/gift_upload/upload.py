MINIO_DOMAIN = "s3-gzpu.didistatic.com"
ACCESS_KEY = "AKDD000000000012TB9NNEF1HS6BMU"
SECRET_KEY = "ASDDTxyzptbKzxYEXhJTlyqGTNsBJFzNLupfKufh"
MINIO_BUCKET = "dedge-material"

import os

try:
    from minio import Minio
    from minio.error import S3Error
except:
    print("import minio error.......")
    os.system('pip3 install minio')
    from minio import Minio
    from minio.error import S3Error


def uploadFile(object_name, file_path):
    # 图片上传
    client = Minio(
        MINIO_DOMAIN,
        access_key=ACCESS_KEY,
        secret_key=SECRET_KEY,
    )
    found = client.bucket_exists(MINIO_BUCKET)
    if not found:
        client.make_bucket(MINIO_BUCKET)
    objectWriteResult = client.fput_object(
        MINIO_BUCKET, "_" + object_name, file_path,
    )
    return "https://" + MINIO_DOMAIN + "/" + MINIO_BUCKET \
           + "/" + objectWriteResult.object_name
