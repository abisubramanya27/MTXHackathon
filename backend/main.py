from ocr import get_ocr_data
from relie import relie
from visualization import ocr_linking_visualization
from bert_classifier import get_predicted_labels
from PIL import Image
import os

def main(img, optional_annot):
    ocr = optional_annot
    if not optional_annot:
        ocr = get_ocr_data(img)
        
    updated_ocr = get_predicted_labels(ocr, os.getenv('BERT_MODEL_PATH'), os.getenv('KNN_MODEL_PATH'))
    
    for box in updated_ocr['form']:
        box['box'] = list(map(lambda x: x * 1000 / img.height, box['box']))
    
    updated_ocr = relie(img,updated_ocr, os.getenv('SCORING_MODEL_PATH'))

    for box in updated_ocr['form']:
        if 'linking' not in box:
            box['linking'] = []
        
    image = ocr_linking_visualization(img,updated_ocr)
    
    return image, updated_ocr
