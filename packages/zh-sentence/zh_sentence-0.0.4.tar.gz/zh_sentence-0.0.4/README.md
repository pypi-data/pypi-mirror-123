A light-weight sentence tokenizer for Chinese languages.

Sample Code:

from zh_sentence.tokenizer import tokenize

paragraph_str = "你好吗？你快乐吗？"

sentence_list = tokenize(paragraph_str)

for sentence in sentence_list:
	print(sentence)
