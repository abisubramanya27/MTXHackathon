from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import torch.nn.functional as F
from torch import nn
from torchsummary import summary
import random
from pprint import pprint


class NeighbourModel(nn.Module):

    def __init__(self, vocab_size, tmp_emb_dim, hidden_dim, max_length, nheads, n_neighbours, pd=0.5, pa=0.1):
        super().__init__()

        self.neighbour_word_embed = nn.Embedding(vocab_size, hidden_dim)
        self.linear1 = nn.Linear(2, tmp_emb_dim)
        self.linear2 = nn.Linear(tmp_emb_dim, hidden_dim)
        self.dropout1 = nn.Dropout(pd)
        self.dropout2 = nn.Dropout(pd)
        self.text_transformer = nn.TransformerEncoderLayer(hidden_dim, nheads, dropout=pa, activation='relu')
        self.linear3 = nn.Linear(hidden_dim*max_length, hidden_dim)
        self.nbr_transformer = nn.TransformerEncoderLayer(hidden_dim*2, nheads, dropout=pa, activation='relu')
        self.linear4 = nn.Linear(hidden_dim*n_neighbours*2, hidden_dim*2)

    def forward(self, words, positions):

        # Text embedding - concatenating word embeddings of a neighbor
        embedding = self.neighbour_word_embed(words)
        n_neighbours = embedding.size()[1]
        bs = embedding.size()[0]
        max_length = embedding.size()[2]
        for i in range(n_neighbours):
            if i == 0:
                text_out = self.text_transformer(embedding[:,i]).view(1,bs,max_length,-1)
            else:
                text_out = torch.cat((text_out, self.text_transformer(embedding[:,i]).view(1,bs,max_length,-1)))

        text_out = torch.transpose(text_out, 0, 1).view(bs,n_neighbours,-1)
        text_out = F.relu(self.linear3(text_out))

        # Position embedding
        pos = F.relu(self.linear1(positions))
        pos = self.dropout1(pos)
        pos = F.relu(self.linear2(pos))
        pos = self.dropout2(pos)

        # Concatenating text and position embeddings
        neighbour_embedding = torch.cat((text_out, pos), dim=2)

        # Transformer - attention + dense layer
        attn_out = self.nbr_transformer(neighbour_embedding)
        result = F.relu(self.linear4(attn_out.view(bs, -1)))

        return result

class ScoreModel(nn.Module):

    def __init__(self, vocab_size, tmp_emb_dim, hidden_dim, max_length, nheads, n_neighbours, pd=0.5, pa=0.1):
        super().__init__()

        self.answer_word_embed = nn.Embedding(vocab_size, hidden_dim)
        self.answer_linear1 = nn.Linear(4, tmp_emb_dim)
        self.answer_linear2 = nn.Linear(tmp_emb_dim, hidden_dim)
        self.answer_dropout1 = nn.Dropout(pd)
        self.answer_dropout2 = nn.Dropout(pd)
        self.answer_transformer = nn.TransformerEncoderLayer(hidden_dim, nheads, dropout=pa, activation='relu')
        self.answer_linear3 = nn.Linear(hidden_dim*max_length, hidden_dim)

        self.question_word_embed = nn.Embedding(vocab_size, hidden_dim)
        self.question_linear1 = nn.Linear(4, tmp_emb_dim)
        self.question_linear2 = nn.Linear(tmp_emb_dim, hidden_dim)
        self.question_dropout1 = nn.Dropout(pd)
        self.question_transformer = nn.TransformerEncoderLayer(hidden_dim, nheads, dropout=pa, activation='relu')
        self.question_linear3 = nn.Linear(hidden_dim*max_length, hidden_dim)

        self.neighbour_network = NeighbourModel(vocab_size, tmp_emb_dim, hidden_dim, max_length, nheads, n_neighbours, pd, pa)
        self.ans_nbr_linear = nn.Linear(hidden_dim*4, hidden_dim*2)

        self.cos_sim = nn.CosineSimilarity(dim=1, eps=1e-6)

    def forward(self, question_text, question_pos, answer_text, answer_pos, neighbour_text, neighbour_pos):
        nbr_result = self.neighbour_network(neighbour_text, neighbour_pos)
        bs = nbr_result.size()[0]

        ans_text_out = self.answer_word_embed(answer_text)
        ans_text_out = self.answer_transformer(ans_text_out).view(bs, -1)
        ans_text_out = self.answer_linear3(ans_text_out)
        ans_pos_out = F.relu(self.answer_linear1(answer_pos))
        ans_pos_out = self.answer_dropout1(ans_pos_out)
        ans_pos_out = F.relu(self.answer_linear2(ans_pos_out)).view(bs, -1)
        ans_out = torch.cat((ans_text_out, ans_pos_out), dim=-1)
        ans_out = self.answer_dropout2(ans_out)

        ans_nbr_out = F.relu(self.ans_nbr_linear(torch.cat((ans_out, nbr_result), dim=-1))).view(bs, -1)

        qn_text_out = self.question_word_embed(question_text)
        qn_text_out = self.question_transformer(qn_text_out).view(bs, -1)
        qn_text_out = self.question_linear3(qn_text_out)
        qn_pos_out = F.relu(self.question_linear1(question_pos))
        qn_pos_out = self.question_dropout1(qn_pos_out)
        qn_pos_out = F.relu(self.question_linear2(qn_pos_out)).view(bs, -1)
        qn_out = torch.cat((qn_text_out, qn_pos_out), dim=-1)

        similarity = self.cos_sim(qn_out, ans_nbr_out).view(bs, -1)
        scores = (similarity + 1) / 2.0


        return scores