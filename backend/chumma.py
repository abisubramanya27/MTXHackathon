from PIL import Image
import numpy as np
import cv2

# img = Image.open('81574683.png').convert('RGB')
# print(type(img))

# ar = np.asarray(img)
# print(ar.shape)

with open('81574683.png', 'rb') as f:
    np_arr = np.frombuffer(f.read(), dtype=np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    print(np_arr.shape)
    print(type(img))
    print(img.shape)