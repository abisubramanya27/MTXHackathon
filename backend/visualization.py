from utils import *

import cv2
from PIL import Image
import numpy as np

def draw_ocr_own(image,
             boxes,
             font_path,color=(255, 0, 0),thick=2):
    """
    Visualize the results of OCR detection and recognition
    args:
        image(Image|array): RGB image
        boxes(list): boxes with shape(N, 4, 2)
        txts(list): the texts
        scores(list): txxs corresponding scores
        drop_score(float): only scores greater than drop_threshold will be visualized
        font_path: the path of font which is used to draw text
    return(array):
        the visualized img
    """

    box_num = len(boxes)
    for i in range(box_num):
        box = np.reshape(np.array(boxes[i]), [-1, 1, 2]).astype(np.int64)
        image = cv2.polylines(np.array(image), [box], True,color , thick)
    return image

def get_bound_box(boxes):
  # print(boxes)
  a = min([box[0] for box in boxes])
  b = min([box[1] for box in boxes])
  c = max([box[2] for box in boxes])
  d = max([box[3] for box in boxes])

def ocr_linking_visualization(img_path,anno,font_path):
  image = Image.open(img_path).convert('RGB')
  labels = ['question','answer','header','other']
  colors = [(255,0,0),(255,255,0),(0,0,255),(0,255,0)]


  for label,color in zip(labels,colors):
    boxes = []
    for box in anno['form']:
      if box['label'] == label:
        a,b,c,d = box['box']
        boxes.append([[a,b],[c,b],[c,d],[a,d]])

    image = draw_ocr_own(image, boxes,font_path,color)
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

  image = draw_ocr_own(image, small_boxes ,font_path,(0,0,0),thick=1)
  image = Image.fromarray(image)
  
  return image