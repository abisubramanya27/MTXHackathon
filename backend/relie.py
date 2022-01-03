from model import *

MAX_LENGTH = 64      #@param {type:"integer"}
HIDDEN_DIM = 768     #@param {type:"integer"}
TMP_EMB_DIM = 768    #@param {type:"integer"}
NHEADS = 4           #@param {type:"integer"}
DROPOUT_ATTN = 0.1   #@param {type:"number"}
DROPOUT_DENSE = 0.5  #@param {type:"number"}
N_NEIGHBOURS = 5     #@param {type:"integer"}
BATCH_SIZE = 64      #@param {type:"integer"}

MODEL_NAME = "bert-base-cased"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


def build_dataset2(question,question_pos,answer,answer_pos,answer_neighb,answer_neighb_pos,X,MAX_LENGTH=64):
  encoding = tokenizer.encode(question, add_special_tokens = True, truncation = True, padding = "max_length", max_length=MAX_LENGTH)
  X['question_text'].append(encoding)
  X['question_pos'].append(question_pos)
  answer_encoding = tokenizer.encode(answer, add_special_tokens = True, truncation = True, padding = "max_length", max_length=MAX_LENGTH)
  X['answer_text'].append(answer_encoding)
  answer_neighbours = answer_neighb
  answer_neighb1 = []
  for text in answer_neighbours:
    answer_neighb1.append(tokenizer.encode(text, add_special_tokens = True, truncation = True, padding = "max_length", max_length=MAX_LENGTH))

  X['answer_pos'].append(answer_pos)
  X['neighbour_text'].append(answer_neighb1)
  X['neighbour_pos'].append(answer_neighb_pos)


def build_dataset(text,box,link,list_of_boxes,neighbour_list,X):
  link_box = list_of_boxes[link]
  answer_neighbours = neighbour_list[link]
  answer_neighb = ['NIL']*5
  answer_neighb_pos = [[0,0]]*5
  for i,id in enumerate(answer_neighbours):
    answer_neighb[i] = text
    a,b = get_rel_pos(list_of_boxes[link],list_of_boxes[id])
    answer_neighb_pos[i] = [a,b]

  build_dataset2(text,box['box'],link_box['text'],link_box['box'],answer_neighb,answer_neighb_pos,X)




def build_model(model_path):
	model = ScoreModel(tokenizer.vocab_size, TMP_EMB_DIM, HIDDEN_DIM, MAX_LENGTH, NHEADS, N_NEIGHBOURS, DROPOUT_DENSE, DROPOUT_ATTN)
	DEVICE = "cpu"
	model.to(DEVICE)
	state_dict = torch.load(model_path, map_location="cpu")
	load_result = model.load_state_dict(state_dict, strict=False)
	print(load_result)
	return model

def prepare_scoring_dataset(image_path,anno,X,Q,N_NEIGHBOURS=5):
  prepare_X(X)
  img = Image.open(image_path)
  width = img.width
  height = img.height
  list_of_boxes = anno['form']
  x_offset = int(width* 0.1)
  y_offset = int(height*0.1)
  neighbour_list = []
  for box in list_of_boxes:
    text = box['text']
    neighbours = find_neighbour(box, list_of_boxes, x_offset, y_offset, width, height)
    temp_neighb_list = []

    #take top N_NEIGHBOURS neighbours based on overlap score and how far it is from our box
    for (id,score) in neighbours:
      a,b = get_rel_pos(box,list_of_boxes[id])
      if a==0 and b==0 :
        continue
      temp_neighb_list.append((id,score,a**2 + b**2))

    neighbours = sorted(temp_neighb_list,key=lambda x:(float(1)/x[1],x[2]))[:N_NEIGHBOURS]
    neighbours = [a for (a,b,c) in neighbours]
    neighbour_list.append(neighbours)
  total_boxes = len(list_of_boxes)
  
  list_of_non_qns = [ind for ind, box in enumerate(list_of_boxes) if box['label'] != 'question']

  for box in list_of_boxes:
    if box['label'] == 'question' :
      text = box['text']
      for link in list_of_non_qns:
        build_dataset(text,box,link,list_of_boxes,neighbour_list,X)
        Q.append([box['id'],link])



def relie(image_path,anno,model_path):
	#model path is path to pytorch_model.bin
	model = build_model(model_path)
	X = {}
	Q = []
	prepare_scoring_dataset(img_path,anno,X,Q)
	keys = X.keys()
	key = [k for k in keys]
	count = 64
	all_preds = []
	for i in tqdm(range(0,len(Q),count)):
	  pred = model.forward(torch.tensor(X[key[0]][i:i+count]).to(DEVICE)
	                                      ,torch.tensor(X[key[1]][i:i+count],dtype=torch.float32).to(DEVICE)
	                                      ,torch.tensor(X[key[2]][i:i+count]).to(DEVICE)
	                                      ,torch.tensor(X[key[3]][i:i+count],dtype=torch.float32).to(DEVICE)
	                                      ,torch.tensor(X[key[4]][i:i+count]).to(DEVICE)
	                                      ,torch.tensor(X[key[5]][i:i+count],dtype=torch.float32).to(DEVICE)
	                                      )
	  all_preds += pred.tolist()

	all_preds = [j[0] for j in all_preds]
	all_preds = np.array(all_preds)
	preds = np.rint(all_preds+0.02)
	for (qid,ansid),score in zip(Q,preds):
	  if score==1:
	    link_list = anno['form'][qid].get('linking',[])
	    link_list.append([qid,ansid])
	    anno['form'][qid]['linking'] = link_list
	    link_list = anno['form'][ansid].get('linking',[])
	    link_list.append([qid,ansid])
	    anno['form'][ansid]['linking'] = link_list

	return anno




