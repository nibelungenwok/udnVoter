import os
from pathlib import Path

from PIL import Image
import pytesseract


images_folder_name = 'ocr_images'
alt_images_folder_path = os.path.join(os.path.curdir, images_folder_name) 
print(alt_images_folder_path)  
abs_images_folder_path = Path(__file__).resolve().with_name(images_folder_name) 
print(abs_images_folder_path)  
exts = ['png', 'jpeg', 'jpg']
images = []

#find all image file in the folder
# assume file name format has only one '.'
#for file_ in os.listdir().sort():
#for file_ in os.listdir():
for file_ in os.listdir(alt_images_folder_path):
#for file_ in os.listdir(abs_images_folder_path):
    print(f'list file: {file_}')
    #print(file)
    if os.path.isfile(os.path.join(alt_images_folder_path, file_)):
        file_parts = file_.split('.')
        print(f'ext: {file_parts[-1]}')
        #if file_parts[-1] in exts:
        if len(file_parts) > 1 and file_parts[-1] in exts:
            print(f'image file: {file_}')
            images.append(file_)
print(f'images: {images}')


url_auto_generate_captch_for_testing = "https://udn.com/funcap/keyimg?random=1593753906000"
url_vote_main_page = 'https://udn.com/func/vote'
'''
r = requests.get(url_auto_generate_captch_for_testing) 
if r.status_code == 200:
    print('server working')
    # save photo

else:
    print('server down')
'''
texts = ['7481','1580','2665']
sorted_images = sorted(images)
image_text_tuples = zip(sorted_images, texts)
# use local image to test
for image, text in image_text_tuples:
    print(f'image: {image}, text:{text}')
    image_path = os.path.join(alt_images_folder_path, image) 
    ocr_text = pytesseract.image_to_string(image_path , lang='eng')
    print(f'ocr_text: {ocr_text}')
    assert ocr_text == text

# user provide path of each file then we return the text
# input image path: return a string of OCR text
def ocr_to_text(image_path):
    img = Image.open(image_path)
    ocr_text = pytesseract.image_to_string(image_path , lang='eng')
    return ocr_text
