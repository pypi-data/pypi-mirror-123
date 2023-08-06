# -*- coding:utf-8 -*-
import numpy as np
from bert_text_pretty import cls,ner,relation,tokenization



text_list = ["你是谁123456"]


tokenizer = tokenization.FullTokenizer(vocab_file=r'F:\pretrain\chinese_L-12_H-768_A-12\vocab.txt',do_lower_case=True)

feat = cls.cls_text_feature(tokenizer,text_list,max_seq_len=128,with_padding=None)
print(feat)

feat = ner.ner_text_feature(tokenizer,text_list,max_seq_len=128,with_padding=None)
print(feat)

feat = relation.re_text_feature(tokenizer,text_list,max_seq_len=128,with_padding=None)
print(feat)


labels = ['标签1','标签2']
print(cls.load_labels(labels))

print(ner.load_label_bio(labels))


# logits 为bert 预测结果
# ner.ner_decoding(text_list,logits,labels,logits)


# logits 为bert 预测结果
# cls.cls_decoding(text_list,logits,labels,logits)


