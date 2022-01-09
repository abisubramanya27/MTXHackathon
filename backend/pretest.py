from main import main
from PIL import Image

img = Image.open('./test_image.png')
main(img, None)