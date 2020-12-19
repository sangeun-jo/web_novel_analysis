from django import forms

GENRE_CHOICES = [('[로판]', '로판'), ('[로맨스]', '로맨스'), ('[BL]', 'BL'), ('[GL]', 'GL'), ('[판타지]', '판타지'), ('[무협]', '무협'), ('[라이트노벨]', '라이트노벨'), ('[추리]', '추리'), ('[팬픽]', '팬픽'), ('[패러디]', '패러디'), ('[문학]', '문학')]
TERM_CHOICES = [(1, '1일'), (7, '1주'), (30, '1개월'), (90, '3개월'), (180,'6개월')]
MONTH_CHOICES= [tuple([x,x]) for x in range(1,13)]
DAY_CHOICES= [tuple([x,x]) for x in range(1,32)]
INTEGER_CHOICES= [tuple([x,x]) for x in range(1,32)]

class optionForm(forms.Form):
	genre = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=GENRE_CHOICES, initial=['판타지', '로맨스', 'BL'])
	#genre = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=GENRE_CHOICES, initial=['판타지', '로맨스', 'BL'])
	#platform= forms.ChoiceField(choices=PLATFORM_CHOICES, initial='all')
	#genre = forms.ChoiceField(choices=GENRE_CHOICES, initial='all')
	term = forms.ChoiceField(choices=TERM_CHOICES, initial='1개월')