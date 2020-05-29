from django import forms

PLATFORM_CHOICES = [('조아라', '조아라'), ('문피아', '문피아'), ('북팔', '북팔') ]
GENRE_CHOICES = [('판타지', '판타지'), ('로맨스', '로맨스'), ('BL','BL')]
TERM_CHOICES = [('1일', '1일'), ('1주', '1주'), ('1개월', '1개월'), ('3개월', '3개월'), ('6개월','6개월')]
MONTH_CHOICES= [tuple([x,x]) for x in range(1,13)]
DAY_CHOICES= [tuple([x,x]) for x in range(1,32)]
INTEGER_CHOICES= [tuple([x,x]) for x in range(1,32)]

class optionForm(forms.Form):
	platform = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=PLATFORM_CHOICES, initial=['조아라', '문피아', '북팔'])
	genre = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=GENRE_CHOICES, initial=['판타지', '로맨스', 'BL'])
	#platform= forms.ChoiceField(choices=PLATFORM_CHOICES, initial='all')
	#genre = forms.ChoiceField(choices=GENRE_CHOICES, initial='all')
	term = forms.ChoiceField(choices=TERM_CHOICES, initial='1개월')