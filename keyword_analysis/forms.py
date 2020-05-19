from django import forms

class SearchForm(forms):
	search_word = forms.Charfield(label='Search Word')