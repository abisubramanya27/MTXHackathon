import torch
from transformers import BertForSequenceClassification, BertTokenizer
import pickle
from torch.utils.data import DataLoader

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

class FUNDSDataset_Inference(torch.utils.data.Dataset):
    def __init__(self, encodings):
        self.encodings = encodings

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]).to(DEVICE) for key, val in self.encodings.items()}
        return item
    
    def __len__(self):
        return len(self.encodings['input_ids'])


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


def inference_model(annotation_inp_file, bert_model_path, knn_model_path):
  tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
  model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=4)
  model.to(DEVICE)
  state_dict = torch.load(bert_model_path, map_location="cpu")
  model.load_state_dict(state_dict, strict=False)
  data=Dataset_Inference(annotation_inp_file)
  text = data.prep()
  encodings = tokenizer(text, truncation=True, padding=True)
  inference_dataloader = DataLoader(FUNDSDataset_Inference(encodings), batch_size=37, drop_last=False)
  X = torch.tensor([]).to(DEVICE)
  for inputs in inference_dataloader:
    X = torch.cat((X, model(**inputs).logits))

  knn_model = pickle.load(open(knn_model_path, 'rb'))
  result = knn_model.predict(X.tolist())
  return result


def get_predicted_labels(anot, bert_model_path, knn_model_path):
  preds = inference_model(anot, bert_model_path, knn_model_path)
  dic={0:'question', 1:'answer', 2:'header', 3:'other'}
  for i in range(len(anot['form'])):
    anot['form'][i]['label'] = dic[preds[i]]

  return anot
