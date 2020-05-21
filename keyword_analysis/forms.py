from django import forms



PLATFORM_CHOICES = [('조아라', '조아라'), ('monpia', '문피아'), ('bookfal', '북팔') ]
GENRE_CHOICES = [('pantazy', '판타지'), ('romance', '로맨스'), ('BL','BL')]
TERM_CHOICES = [('1일', '1일'), ('week', '1주'), ('_1month', '1개월'), ('_3month', '3개월'), ('_6month','6개월')]
MONTH_CHOICES= [tuple([x,x]) for x in range(1,13)]
DAY_CHOICES= [tuple([x,x]) for x in range(1,32)]
INTEGER_CHOICES= [tuple([x,x]) for x in range(1,32)]

class optionForm(forms.Form):
	#platform = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=PLATFORM_CHOICES, initial=['joara', 'monpia', 'bookfal'])
	#genre = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=GENRE_CHOICES, initial=['pantazy', 'romance', 'BL'])
	platform= forms.ChoiceField(choices=PLATFORM_CHOICES, initial='조아라', )
	genre = forms.ChoiceField(choices=GENRE_CHOICES, initial='all')
	term = forms.ChoiceField(choices=TERM_CHOICES, initial='_1month')