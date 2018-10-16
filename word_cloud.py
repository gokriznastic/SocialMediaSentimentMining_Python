import numpy as np # linear algebra
import pandas as pd 
import matplotlib as mpl
import matplotlib.pyplot as plt

from subprocess import check_output
from wordcloud import WordCloud, STOPWORDS

#mpl.rcParams['figure.figsize']=(8.0,6.0)    #(6.0,4.0)
mpl.rcParams['font.size']=12                #10 
mpl.rcParams['savefig.dpi']=100             #72 
mpl.rcParams['figure.subplot.bottom']=.1 

class word_cloud(object):
	def plot(self,input_csv,output_png):
		stopwords = set(STOPWORDS)
		data = pd.read_csv(input_csv)

		wordcloud = WordCloud(
				          background_color='white',
				          stopwords=stopwords,
				          max_words=200,
				          max_font_size=40, 
				          random_state=42
				         ).generate(str(data['text']))

		print(wordcloud)
		fig = plt.figure(1)
		plt.imshow(wordcloud)
		plt.axis('off')
		plt.show()
		fig.savefig(output_png, dpi=900)
