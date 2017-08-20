#!/usr/bin/env python

import os

import matplotlib.pyplot as plt
import numpy
from PIL import Image
from wordcloud import WordCloud, STOPWORDS

d = os.path.dirname(__file__)

alice_mask = numpy.array(Image.open(os.path.join(d, 'alice_mask.png')))

stopwords = set(STOPWORDS)
stopwords.add('said')

word_cloud = WordCloud(background_color='white', max_words=2000, mask=alice_mask, stopwords=stopwords)

text = open(os.path.join(d, 'alice.txt')).read()

word_cloud.generate(text)

word_cloud.to_file(os.path.join(d, 'alice.png'))

plt.imshow(word_cloud, interpolation='bilinear')
plt.axis('off')

plt.figure()

plt.imshow(alice_mask, cmap=plt.cm.gray, interpolation='bilinear')
plt.axis('off')

plt.show()
