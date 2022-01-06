from ocr import get_ocr_data
from relie import relie
from visualization import ocr_linking_visualization
from bert_classifier import get_predicted_labels
from PIL import Image

img_path = '81574683.png'
ocr = get_ocr_data(img_path)
updated_ocr = get_predicted_labels(ocr)
updated_ocr = relie(img_path,updated_ocr,'../../Hackathons/MTX/results/best_model/pytorch_model.bin')

image = ocr_linking_visualization(img_path,updated_ocr,'simfang.ttf')
image = Image.fromarray(image)
image.save('output.png')
