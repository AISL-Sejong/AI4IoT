import base64
import sys
import os.path
import io
from PIL import Image

def decode_img(msg):
    msg = base64.b64decode(msg)
    buf = io.BytesIO(msg)
    img = Image.open(buf)
    return(img)
    
