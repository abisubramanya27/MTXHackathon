from ocr import get_ocr_data
from relie import relie
from visualization import ocr_linking_visualization

from PIL import Image

img_path = '81574683.png'
ocr = get_ocr_data(img_path)

updated_ocr = relie(img_path,ocr,'model.bin')

image = ocr_linking_visualization(img_path,updated_ocr,'simfang.ttf')
image = Image.fromarray(image)
image.save('output.png')