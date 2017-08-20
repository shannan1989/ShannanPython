#!/usr/bin/env python

import os

import matplotlib.pyplot as plt
from wordcloud import WordCloud

d = os.path.dirname(__file__)

text = open(os.path.join(d, 'I have a dream.txt')).read()

word_cloud1 = WordCloud().generate(text)

# lower max_font_size
word_cloud2 = WordCloud(max_font_size=40).generate(text)

# Display the generated image:

# the matplotlib way:

plt.imshow(word_cloud1, interpolation='bilinear')
plt.axis("off")

plt.figure()

plt.imshow(word_cloud2, interpolation="bilinear")
plt.axis("off")

plt.show()

# The pil way

image = word_cloud1.to_image()
image.show()
