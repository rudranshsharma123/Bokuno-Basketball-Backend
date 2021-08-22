import os
from flask import Flask, request, jsonify, make_response
import random
from jina import Document
from werkzeug.serving import WSGIRequestHandler
import base64
# from cockroach import Cockroach
import io
from PIL import Image

from datetime import datetime

from werkzeug.utils import send_file
from werkzeug.wrappers import response
app = Flask(__name__)

@app.route('/') # this is the home page route
def hello_world(): # this is the home page function that generates the page code
    return "Hello world!"


def fetchImageJina(imageName):
  '''
  Use this function to search for Images similar to that image. It takes in the name of the image. The name as which it is saved as in the disk.
  Then this function will send the best match Jina could find
  '''
  import cv2
  import requests
  x = cv2.imread(imageName)
  doc = Document(content = x)
  doc.convert_image_blob_to_uri(width=100, height=100)
  headers = {
        'Content-Type': 'application/json',
    }
  data = '{"top_k":1,"mode":"search","data":["' + doc.uri + '"]}'

  response = requests.post(
          'http://172.26.75.96:45678/search', headers=headers, data=data)
  res = response.json()
  return res["data"]['docs'][0]['matches'][0]['text']

def fetchTextJina(searchText):
  '''
  Use this function to search for images in Jina. This function takes in the text for which you would like to search the images for.
  Try Calling this function as fetchImageJina("BasketBall") and this function will return the best image match. It will save the best match image in the disk
  and return the name of the image which it is saved as
  '''
  
  import requests
  import cv2
  text = searchText
  headers = {
        'Content-Type': 'application/json',
    }
  data = '{"top_k":1,"mode":"search","data":["' + text + '"]}'
  response = requests.post(
          'http://172.26.75.96:45678/search', headers=headers, data=data)
  res = response.json()

  b64_string = res['data']['docs'][0]['matches'][0]
  doc = Document(b64_string)
  doc.convert_image_datauri_to_blob()
  cv2.imwrite("search.jpg", cv2.cvtColor(doc.blob, cv2.COLOR_RGB2BGR))
  return "search.jpg"

def fetchAns(text):
  import requests
  headers = {
        'Content-Type': 'application/json',
    }

  data = '{"top_k":1,"mode":"search","data":["' + text + '"]}'

  response = requests.post(
        'http://172.26.75.96:34567/search', headers=headers, data=data)

  res = response.json()
  return_text = res["data"]['docs'][0]['matches'][0]['tags']['ans']
  return return_text
    


@app.route('/chat', methods = ['POST'])
def chat():
  response = request.get_json(silent= True, force= True)
  # res = response.json()
  return fetchAns(response['ask'])



@app.route('/image', methods = ['POST' , 'GET'])
def hola():
    image = request.files['picture']
    image_name = image.filename
    image.save(os.path.join(os.getcwd(), image_name))
    return_text = fetchImageJina(image_name)
    return jsonify({'ans':return_text})


@app.route('/send', methods= ['GET'])
def send():
  with open("1.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read())
  with open("2.jpg", "rb") as image_file:
    encoded_string2 = base64.b64encode(image_file.read())
  
  x = [str(encoded_string2), str(encoded_string)]
  return jsonify({'images':x})

@app.route('/search', methods=['POST'])
def search():
  response = request.get_json(force= True, silent= True)
  print(response['search'])
  return_image = fetchTextJina(response['search'])
  
  with open(return_image, 'rb') as image_file:
    encoded_string = base64.b64encode(image_file.read())
  return jsonify({'image':[str(encoded_string)]})


  
  
  return "done"
    


if __name__ == '__main__':
  WSGIRequestHandler.protocol_version = "HTTP/1.1"
  app.run(host='0.0.0.0', port=12345) # This line is required to run Flask on repl.it 




#Commented Code
#1 
#def hola():
 # x = io.BytesIO(image)
    # # cv2.namedWindow('Image')
    # x = cv2.imread("1.jpg")
    # # img = Image.open('1.jpg', mode = 'r')
    # byte_arr = io.BytesIO(image)
    # base64.encodebytes(byte_arr.getvalue()).decode('ascii')
      # x = cv2.imread(image_name)
    

    # print(len(encoded_string))
    # x = [str(encoded_string2), str(encoded_string)]
    
    # # cv2.imshow(x, mat=)
    # # window_name = 'image'
    # cv2.imshow('Image', x)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # print(x.getvalue())