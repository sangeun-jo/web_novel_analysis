from django import forms

GENRE_CHOICES = [('판타지', '판타지'), ('로맨스', '로맨스'), ('로맨스판타지', '로맨스판타지'), ('무협', '무협'), ('퓨전', '퓨전'), ('게임', '게임'), ('역사', '역사'), ('스포츠', '스포츠'), ('라이트노벨', '라이트노벨'), ('BL','BL'), ('GL', 'GL'), ('패러디', '패러디'), ('팬픽', '팬픽'), ('SF', 'SF'), ('밀리터리', '밀리터리'), ('시', '시'), ('소설', '소설'), ('수필', '수필'), ('공포', '공포'), ('추리', '추리'), ('아동', '아동'), ('시나리오/희곡', '시나리오/희곡'), ('비평', '비평')]
TERM_CHOICES = [(1, '1일'), (7, '1주'), (30, '1개월'), (90, '3개월'), (180,'6개월')]
MONTH_CHOICES= [tuple([x,x]) for x in range(1,13)]
DAY_CHOICES= [tuple([x,x]) for x in range(1,32)]
INTEGER_CHOICES= [tuple([x,x]) for x in range(1,32)]

class optionForm(forms.Form):
	genre = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=GENRE_CHOICES)
	#platform= forms.ChoiceField(choices=PLATFORM_CHOICES, initial='all')
	#genre = forms.ChoiceField(choices=GENRE_CHOICES, initial='all')
	term = forms.ChoiceField(choices=TERM_CHOICES, initial=30)