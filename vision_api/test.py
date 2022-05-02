import os,io
from google.cloud import vision_v1
from google.cloud.vision_v1 import types
import pandas as pd

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'C:\Projects\Resume\Resume_Parser\vision_api\vision_api_key.json'

client = vision_v1.ImageAnnotatorClient()
FILE_NAME = 'ABHINAV KUMAR2_page-0001.jpg'
FOLDER_PATH = r'C:/Projects/Resume/Resume_Parser/vision_api/'
with io.open(os.path.join(FOLDER_PATH,FILE_NAME),'rb') as image_file:
    content = image_file.read()
    print(content)
image = vision_v1.types.Image(content=content)
response = client.text_detection(image=image)
texts = response.text_annotations
# print(texts)  
df = pd.DataFrame(columns=['locale','description'])
for text in texts:
      df = df.append(
          dict(
              locale = text.locale,
              description = text.description
          ),
          ignore_index = True
      )  
print(type(df['description'][0]))
