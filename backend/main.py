from ocr import get_ocr_data
from relie import relie
from visualization import ocr_linking_visualization
from bert_classifier import get_predicted_labels
from PIL import Image
import os

img_path = '81574683.png'
img = Image.open(img_path)
ocr = get_ocr_data(img)
updated_ocr = get_predicted_labels(ocr, os.getenv('BERT_MODEL_PATH'), os.getenv('KNN_MODEL_PATH'))
updated_ocr = relie(img,updated_ocr, os.getenv('SCORING_MODEL_PATH'))

image = ocr_linking_visualization(img,updated_ocr,'simfang.ttf')
image = Image.fromarray(image)
image.save('output.png')
