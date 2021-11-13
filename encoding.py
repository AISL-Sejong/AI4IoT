import base64
import sys
import os.path
import io
from PIL import Image

def encode_img(filename):
    with open(filename, "rb") as imageFile:
        msg = base64.b64encode(imageFile.read())
    return msg