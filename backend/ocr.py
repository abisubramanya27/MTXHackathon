from paddleocr import PaddleOCR
from textblob import TextBlob
from wordsegment import load, segment
import numpy as np

load()


def get_json(text,box,id):
  temp_json = {}
  temp_json['text'] = text
  temp_json['box'] = box
  temp_json['id'] = id
  return temp_json

def process_ocr_text(text):
  words = text.split(' ')
  text = ''
  for word in words:
    if not all(c.isalpha() for c in word):
      text += word
      text += ' '
      if word != words[-1]: text += ' '
      continue
    blob_text = TextBlob(word)
    word = blob_text.correct()
    word = str(word)
    ss = segment(word)
    text += word[:len(ss[0])]
    word = word[len(ss[0]):]
    for indd in range(1,len(ss)):
      text += ' '
      text += word[:len(ss[indd])]
      word = word[len(ss[indd]):]

    if word != words[-1]: text += ' '

  return text



def get_ocr_data(image):
  img_arr = np.asarray(image.convert('RGB'))[:,:,::-1]
  ocr = PaddleOCR(use_angle_cls=True,lang ='en',show_log=False)
  result = ocr.ocr(img_arr,cls=True)
  tot_json = {}
  tot_json['form'] = []
  count = 0
  for j in result:
    a,b = j
    p1,_,p3,_ = a
    text,sc = b
    if sc > 0.9 :
      text = process_ocr_text(text)

    if any(c.isalpha() for c in text):
      text_list = text.split(':')
      val = -1
      for i in range(len(text_list)-2,-1,-1):
        temp_text = text_list[i]
        if any(c.isalpha() for c in temp_text) :
          val = i
          break
      text_list[val+1] = ':'.join(text_list[val+1:])
      text_list = text_list[:val+2]
      ll = len(text)
      width = p3[0] - p1[0]
      s1 = p1[0]
      for text_part in text_list[:-1]:
        s2 = s1 + (len(text_part)+1)*width/ll
        s2 = int(s2)
        tot_json['form'].append(get_json(text_part+':',[s1,p1[1],s2,p3[1]],count))
        count += 1
        s1 = s2
      if text_list[-1]=='':
        continue
      s2 = p3[0]
      tot_json['form'].append(get_json(text_list[-1],[s1,p1[1],s2,p3[1]],count))
      count += 1
    else :
      tot_json['form'].append(get_json(text,[p1[0],p1[1],p3[0],p3[1]],count))
      count += 1

  return tot_json