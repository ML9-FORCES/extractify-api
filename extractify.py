from transformers import BertTokenizer
import tensorflow as tf
import numpy as np
import json
import gdown
import os

class bert_classifier:
    def __init__(self):
        self.model = tf.keras.models.load_model('./MODELS/bert_classifier')
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-cased')


    def preprocessing(self, input_data):
        tokens = self.tokenizer.encode_plus(input_data, max_length=50,
                                   truncation=True, padding='max_length',
                                   add_special_tokens=True, return_token_type_ids=False,
                                   return_tensors='tf')
        # tokenizer returns int32 tensors, we need to return float64, so we use tf.cast
        in_tensor = {'input_ids': tf.cast(tokens['input_ids'], tf.float64),
            'attention_mask': tf.cast(tokens['attention_mask'], tf.float64)}
        return in_tensor 

    def predict(self, input_data):
        return self.model.predict(input_data)[0]

    def postprocessing(self, input_data):
        bins={1:'key',2:'value',0:'other'}
        return bins[np.argmax(input_data)],str(np.max(input_data))

    def compute_prediction(self, input_data):
        try:
            input_data = self.preprocessing(input_data)
            prediction = self.predict(input_data)
            prediction = self.postprocessing(prediction)
        except Exception as e:
            return {"status": "Error", "message": str(e)}

        return prediction

class linking_classifier:
  def __init__(self):
    self.model = tf.keras.models.load_model('./MODELS/linking')  
 
  def ext(self,box):
    width=box[2]-box[0]
    height=box[3]-box[1]
    c_x=(box[0]+box[2])/2
    c_y=(box[1]+box[3])/2
    return c_x,c_y,width,height

  def preprocessing(self, input_data1,input_data2):
    b1=self.ext(input_data1)
    b2=self.ext(input_data2)
    dis=(b1[0]-b2[0])**2 + (b1[1]-b2[1])**2
    dis=dis**0.5
    sin=(b1[1]-b2[1])/dis
    sin*= -1 if sin<0 else 1
    relative_width = b1[2]/b2[2] if b2[2]>b1[2] else b2[2]/b1[2]
    relative_height = b1[3]/b2[3] if b2[3]>b1[3] else b2[3]/b1[3]
    return [dis/1000,sin,relative_width,relative_height]

  def predict(self, input_data):
    return self.model.predict(np.array([input_data]))[0]

  def postprocessing(self, input_data):
    bins={1:'linked',0:'unlinked'}
    return bins[np.argmax(input_data)],str(np.max(input_data))

  def compute_prediction(self, input_data1,input_data2):
    try:
      input_data = self.preprocessing(input_data1,input_data2)
      prediction = self.predict(input_data)
      prediction = self.postprocessing(prediction)
    except Exception as e:
      return {"status": "Error", "message": str(e)}
    return prediction

class Wrapper:
  def __init__(self,classifier,linker):
    self.data = None
    self.classifier = classifier
    self.linker=linker
    self.keys=[]
    self.values=[]

  def preprocessing(self,json):
    self.data=json
    try:
      for i in self.data:
        del i['label']
        del i ['linking']
    except:
      pass

  def classification(self):
    for i in self.data['form']:
      i['linking']=[]
      i['label']=list(self.classifier.compute_prediction(i['text']))
      if i['label'][0]=='key':
        self.keys.append(i['id'])
      if i['label'][0]=='value':
        self.values.append(i['id'])

  def linking(self):
    for i in self.keys:
      for j in self.values:
        link = list(self.linker.compute_prediction(self.data['form'][i]['box'],self.data['form'][j]['box']))
        if link[0] == 'linked':
          self.data['form'][i]['linking'].append([i,j,link[1]])
          self.data['form'][j]['linking'].append([i,j,link[1]])

  def generate(self,json):
    self.preprocessing(json)
    self.classification()
    self.linking()
    return self.data

url='https://drive.google.com/drive/folders/1UjpkmlaFIExoE4slCLdaEAxjTBOZ28Fy'
if not os.path.isdir('./MODELS'):
  gdown.download_folder(url,output='./MODELS', quiet=True)

classifier = bert_classifier()
linker = linking_classifier() 
wrapper = Wrapper(classifier,linker)

def generate(json):
  return wrapper.generate(json)
