from django.shortcuts import render
from joara.models import TodayBest
import re
from konlpy.tag import Twitter
from collections import Counter
import urllib, base64
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import io

def pie_graph(qs):
	font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
	rc('font', family=font_name)
	genre = []
	for nov in qs:
		nov.genre
		genre.append(nov.genre)
		rat = Counter(genre)
	group_name = []
	group_size = []
	for genre in rat:
		group_size.append(rat[genre])
		genre = genre.replace('[', '')
		genre = genre.replace(']', '')
		group_name.append(genre)
	plt.figure(figsize=(3.5, 30))
	plt.pie(group_size, 
		labels=group_name, 
		autopct='%1.2f%%', # second decimal place
		shadow=True, 
		#startangle=90,
		textprops={'fontsize': 8}) # text font size
	plt.axis('equal') #  equal length of X and Y axis
	#plt.title('인기 장르', fontsize=20)
	plt.axis("off")
	image = io.BytesIO()
	plt.savefig(image, format='png')
	image.seek(0)  # rewind the data
	string = base64.b64encode(image.read())
	image_64 = 'data:image/png;base64,' + urllib.parse.quote(string)
	return image_64