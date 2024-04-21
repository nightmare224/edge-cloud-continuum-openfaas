import boto3
import re
from os import makedirs, listdir
from os.path import exists, join

def get_secret_by_key(key):
    with open(f"/var/openfaas/secrets/{key}") as f:
        return f.read().strip()


def is_dowloaded_onnx_slice_from_s3(s3_bucket_name, s3_object_name, model_name):
    FILE_PATH = f"/tmp/models/{model_name}/"
    FILE_NAME = join(FILE_PATH, f"{model_name}.onnx")

    return exists(FILE_NAME)

def download_onnx_slice_from_s3(s3_bucket_name, s3_object_name, model_name):
    FILE_PATH = f"/tmp/models/{model_name}/"
    FILE_NAME = join(FILE_PATH, f"{model_name}.onnx")
    if exists(FILE_NAME):
        return FILE_NAME

    makedirs(FILE_PATH, 0o755, exist_ok=True)
    downloading = False
    for filename in listdir(FILE_PATH):
        if filename.startswith(model_name):
            downloading = True
            break

    # not download yet
    if not downloading:
        s3.download_file(s3_bucket_name, s3_object_name, FILE_NAME)
    
    # wait until download is donw
    while not exists(FILE_NAME):
        pass

    return FILE_NAME

s3 = boto3.client(
    's3',
    aws_access_key_id=get_secret_by_key("aws-access-key-id"),
    aws_secret_access_key=get_secret_by_key("aws-secret-access-key"))

# s3 = boto3.client(
#     's3',
#     aws_access_key_id="AKIA6GBMBFTJTXBXQLMF",
#     aws_secret_access_key="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")

download_onnx_slice_from_s3("faas-workload-model-decomposition","resnet50-v1-12.onnx","resnet50-v1-12")