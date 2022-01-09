from utils import get_bound_box,get_links

import cv2
from PIL import Image
import numpy as np

def draw_ocr_own(image, boxes, color=(255, 0, 0), thick=2):
    """
    Visualize the results of OCR detection and recognition
    args:
        image(Image|array): RGB image
        boxes(list): boxes with shape(N, 4, 2)
        color: the color of the bounding box
        thick(int): thickness
    return(array):
        the visualized img
    """

    box_num = len(boxes)
    for i in range(box_num):
        box = np.reshape(np.array(boxes[i]), [-1, 1, 2]).astype(np.int32)
        image = cv2.polylines(np.array(image, dtype=np.uint8), [box], True, color , thick)
    return np.array(image, dtype=np.uint8)


def ocr_linking_visualization(image,anno):
  image = image.convert('RGB')
  labels = ['question','answer','header','other']
  colors = [(255,0,0),(255,255,0),(0,0,255),(0,255,0)]


  for label,color in zip(labels,colors):
    boxes = []
    for box in anno['form']:
      if box['label'] == label:
        a,b,c,d = box['box']
        boxes.append([[a,b],[c,b],[c,d],[a,d]])

    image = draw_ocr_own(image, boxes, color)
    print(type(image))
    image = Image.fromarray(image)


  small_boxes = []
  for i in range(len(anno['form'])):
    box = anno['form'][i]
    if box['label']!='question' and box['label']!='header':
      continue
    if box['linking']==[]:
      continue
    links = [i]+get_links(box['linking'],i)
    if box['label']=='question':
      temp_box = get_bound_box([anno['form'][j]['box'] for j in links if anno['form'][j]['label']!='header' ])
    else :
      temp_box = get_bound_box([anno['form'][j]['box'] for j in links ])
    small_boxes.append(temp_box)

  image = draw_ocr_own(image, small_boxes, (0,0,0), thick=1)
  
  return Image.fromarray(image)