from django.shortcuts import render
from .forms import UploadFileForm
from django.views.decorators.csrf import csrf_exempt
import re, io
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import urllib, base64

def main(request):
	form = UploadFileForm
	return render(request, 'relation/analysis.html', {'form':form})

@csrf_exempt
def result(request):
	try:
		uploadFile = request.FILES['uploadedFile'].read().decode('utf-8')
	except:
		return render(request, 'relation/analysis.html')

	result = relationship(uploadFile, characters(request))
	return render(request, 'relation/analysis.html', {'result':result})

@csrf_exempt
def characters(request):
	try:
		char = request.POST.get('input_char')
	except:
		return render(request, 'relation/analysis.html')
	charlist = char.split(',')
	new_char = []
	for char in charlist:
		new_char.append(char.strip())
	return new_char
	
def relationship(book_text, input_char):

	sections = book_text.split('\n')

	cleaned_sections = []

	for section in sections:
		quotes = re.findall("“.*?”", section)
		for quote in quotes:
			section = section.replace(quote, " ")
		cleaned_sections.append(section)

	characters = input_char
	characters = [character.title() for character in characters]

	sections_dictionary = {}
	iterative = 0
	for section in cleaned_sections:
		iterative += 1
		for char in characters:
			if char in section:
				if str(iterative) in sections_dictionary.keys():
					sections_dictionary[str(iterative)].append(char)  
				else:
					sections_dictionary[str(iterative)] = [char]   

	df = pd.DataFrame(columns = characters, index = characters)
	df[:] = int(0)

	for value in sections_dictionary.values():
		for character1 in characters:
			for character2 in characters:
				if character1 in value and character2 in value:
					df[character1][character2] += 1
					df[character2][character1] += 1
	
	edge_list = []

	for index, row in df.iterrows():
		i = 0
		for col in row:
			weight = float(col)/464
			edge_list.append((index, df.columns[i], weight))
			i += 1

	updated_edge_list = [x for x in edge_list if not x[2] == 0.0]
	
	node_list = []
	for i in characters:
		for e in updated_edge_list:
			if i == e[0] and i == e[1]:
				node_list.append((i, e[2]*6))
	for i in node_list:
		if i[1] == 0.0:
			node_list.remove(i)

	for i in updated_edge_list:
		if i[0] == i[1]:
			updated_edge_list.remove(i)

	plt.subplots(figsize=(14,10))

	G = nx.Graph()
	for i in sorted(node_list):
		G.add_node(i[0], size = i[1])
	G.add_weighted_edges_from(updated_edge_list)

	node_order = characters

	updated_node_order = []
	for i in node_order:
		for x in node_list:
			if x[0] == i:
				updated_node_order.append(x)
    
	test = nx.get_edge_attributes(G, 'weight')
	updated_again_edges = []
	for i in nx.edges(G):
		for x in test.keys():
			if i[0] == x[0] and i[1] == x[1]:
				updated_again_edges.append(test[x])

	node_scalar = 800
	edge_scalar = 10
	sizes = [x[1]*node_scalar for x in updated_node_order]
	widths = [x*edge_scalar for x in updated_again_edges]

	pos = nx.spring_layout(G, k=0.42, iterations=17)

	nx.draw(G, pos, with_labels=True, font_family="NanumBarunGothic", font_size = 8, font_weight = 'bold', node_size = sizes, width = widths)

	plt.axis("off")
	image = io.BytesIO()
	plt.savefig(image, format='png')
	image.seek(0)  # rewind the data
	string = base64.b64encode(image.read())
	image_64 = 'data:image/png;base64,' + urllib.parse.quote(string)
	return image_64