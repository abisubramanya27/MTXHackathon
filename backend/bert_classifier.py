import torch
from transformers import BertForSequenceClassification, BertTokenizer

from transformers import TextClassificationPipeline
import pickle

class FUNDSDataset_Inference(torch.utils.data.Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        return item


class Dataset_Inference():
    def __init__(self, anot):
        self.anot= anot

    def __iter__(self):
      yield self.anot
    def __len__(self):
      return 1
      
    def prep(self):
      anot=self.anot
      txt=[]
      for block in list(anot.values())[0]:
        txt.append(block['text'])
      return txt


def inference_model(annotation_inp_file):
  tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
  model = BertForSequenceClassification.from_pretrained('/content/drive/MyDrive/results/checkpoint-1855',local_files_only=True)
  data=Dataset_Inference(annotation_inp_file)
  text = data.prep()
  pipe = TextClassificationPipeline(model=model, tokenizer=tokenizer, return_all_scores=True)
  X=[]
  for txt in text:
    res = pipe(txt)
    x1=res[0][0]['score']
    x2=res[0][1]['score']
    x3=res[0][2]['score']
    x4=res[0][3]['score']
    X.append(list([x1,x2,x3,x4]))
  knn_model = pickle.load(open('/content/drive/MyDrive/KNN/knn_model', 'rb'))
  result = knn_model.predict(X) 
  return result


def get_predicted_labels(anot):
  preds = inference_model(anot)
  dic={0:'question', 1:'answer', 2:'header', 3:'other'}
  for i in range(len(anot['form'])):
    anot['form'][i]['label'] = dic[preds[i]]

  return anot