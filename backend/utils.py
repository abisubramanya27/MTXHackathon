def get_links(l,id):
  links = []
  for i in l:
    if i[0]==id:
      links.append(i[1])
    else :
      links.append(i[0])

  return links

def get_bound_box(boxes):
  # print(boxes)
  a = min([box[0] for box in boxes])
  b = min([box[1] for box in boxes])
  c = max([box[2] for box in boxes])
  d = max([box[3] for box in boxes])

  return [[a,b],[c,b],[c,d],[a,d]]

#relative position of neighbour
def get_rel_pos(box1,box2):
  x1a,y1a,x2a,y2a = box1['box']
  x1b,y1b,x2b,y2b = box2['box']

  return  ( (x1b + x2b)//2 - (x1a+x2a)//2 , (y1b + y2b)//2 - (y1a+y2a)//2   )

def bb_intersection_over_boxB(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])

    # compute the area of intersection rectangle
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)
    iou = interArea / float(boxBArea)

    # return the intersection over union value
    return iou

def find_neighbour(cad, words, x_offset, y_offset, width, height):
    neighbours = []

    neighbour_x1 = cad['box'][0] - x_offset
    neighbour_x1 = 1 if neighbour_x1 < 1 else neighbour_x1

    neighbour_y1 = cad['box'][1] - y_offset
    neighbour_y1 = 1 if neighbour_y1 < 1 else neighbour_y1

    neighbour_x2 = cad['box'][2] + x_offset
    neighbour_x2 = width - 1 if neighbour_x2 >= width else neighbour_x2

    neighbour_y2 = cad['box'][3] + y_offset
    neighbour_y2 = height - 1 if neighbour_y2 >= height else neighbour_y2

    neighbour_bbox = [neighbour_x1, neighbour_y1, neighbour_x2, neighbour_y2]
    iou_scores = []
    for w in words:
        iou_scores.append(bb_intersection_over_boxB(neighbour_bbox, w['box']))

    for i, iou in enumerate(iou_scores):
        if iou > 0.5:
            neighbours.append((words[i]['id'],iou))

    return neighbours



def Diff(l1,l2):
  return [i for i in l1 if i not in l2]

def prepare_X(X):
  X['question_text'] = []
  X['question_pos'] = []
  X['answer_text'] = []
  X['answer_pos'] = []
  X['neighbour_text'] = []
  X['neighbour_pos'] = []


