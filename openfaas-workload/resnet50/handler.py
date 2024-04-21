from onnxruntime import InferenceSession
from PIL import Image
import numpy as np

from .s3manager import download_onnx_slice_from_s3, is_dowloaded_onnx_slice_from_s3
from os import environ
import io


def handle(event, context):
    if event.path == "/model-readiness":
        if is_dowloaded_onnx_slice_from_s3(s3_bucket_name, s3_object_name, model_name):
            resp = {
                "statusCode": 200
            }
        else:
            resp = {
                "statusCode": 500,
                "body": "The model is downloading..."
            }
        return resp

    input_value = preprocessing(event.body)
    # model_filepath = download_onnx_slice_from_s3(s3_bucket_name, s3_object_name, model_name)
    output_value = inference(model_filepath, input_value)

    return str(interpret_result(output_value))


def inference(model_filepath, input_value):
    session = InferenceSession(model_filepath)
    input_name = session.get_inputs()[0].name
    # only one input
    result = session.run([], {input_name: input_value})[0]
    return result


# for resnet50
def preprocessing(input: bytes):
    img = Image.open(io.BytesIO(input)).resize((224, 224))
    # normalize
    x = np.array(img, dtype='f')[:,:,:3]/255
    #  transpose it from HWC to CHW layout
    x = np.moveaxis(x,-1,0)
    x = np.expand_dims(x, axis=0)

    return x

# for resnet50
def interpret_result(result):
    scores = result[0]

    return np.argmax(scores)

model_name = environ["model_name"]
s3_bucket_name = environ["s3_bucket_name"]
s3_object_name = environ["s3_object_name"]
model_filepath = download_onnx_slice_from_s3(s3_bucket_name, s3_object_name, model_name)
