from django.shortcuts import render
import requests
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib import font_manager, rc
import re, io
import urllib, base64

def home(request): 

	money = [100, 200, 500, 1800, 2700, 4000]
	year = ['2013', '2014', '2015', '2016', '2017', '2018']
	index = np.arange(len(year))
	try:
		font_name = font_manager.FontProperties(fname="C:/Windows/Fonts/malgun.ttf").get_name()
	except:
		font_name = font_manager.FontProperties(fname="/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf").get_name()
	rc('font', family=font_name, size=8)
	plt.figure(figsize=(7, 3.9))
	plt.bar(index, money)
	plt.xlabel('년도')
	plt.ylabel('시장규모(억)')
	plt.xticks(index, year)
	
	image = io.BytesIO()
	plt.savefig(image, format='png', bbox_inches='tight', pad_inches=0.1)
	image.seek(0)  
	string = base64.b64encode(image.read())
	bar_graph = 'data:image/png;base64,' + urllib.parse.quote(string)

	return render(request, 'index.html', {'bar_graph':bar_graph})
