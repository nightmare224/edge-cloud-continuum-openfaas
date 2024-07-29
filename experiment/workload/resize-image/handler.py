import cv2
import numpy as np
import requests
import time

def handle(req):
    start_time = time.time()
    # Open a connection to the URL
    url = req
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Ensure the request was successful

    image_array = np.asarray(bytearray(response.content), dtype=np.uint8)

    # Decode the image array using OpenCV
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    original_height, original_width = image.shape[:2]
    resized_image = cv2.resize(image, (original_height * 2, original_width * 2))

    end_time = time.time()

    # Calculate and print the time taken
    elapsed_time = end_time - start_time
    return f"Time taken to execute the entire function is: {elapsed_time:.4f} seconds"
