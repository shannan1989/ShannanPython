#!/usr/bin/env python
"""
Image-colored wordcloud
=======================
You can color a word-cloud by using an image-based coloring strategy
implemented in ImageColorGenerator. It uses the average color of the region
occupied by the word in a source image. You can combine this with masking -
pure-white will be interpreted as 'don't occupy' by the WordCloud object when
passed as mask.
If you want white as a legal color, you can just pass a different image to
"mask", but make sure the image shapes line up.
"""

import os

import matplotlib.pyplot as plt
import numpy
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

d = os.path.dirname(__file__)

alice_coloring = numpy.array(Image.open(os.path.join(d, "alice_color.png")))

stopwords = set(STOPWORDS)
stopwords.add("said")

word_cloud = WordCloud(background_color="white", max_words=2000, mask=alice_coloring, stopwords=stopwords,
                       max_font_size=40, random_state=42)

text = open(os.path.join(d, 'alice.txt')).read()

word_cloud.generate(text)

plt.imshow(word_cloud, interpolation='bilinear')
plt.axis('off')

plt.figure()

# recolor wordcloud and show
# we could also give color_func=image_colors directly in the constructor

# create coloring from image
image_colors = ImageColorGenerator(alice_coloring)
word_cloud.recolor(color_func=image_colors)

plt.imshow(word_cloud, interpolation='bilinear')
plt.axis('off')

plt.figure()

plt.imshow(alice_coloring, cmap=plt.cm.gray, interpolation='bilinear')
plt.axis('off')

plt.show()
