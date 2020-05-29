from django import forms

BEST_CHOICES = [('web', '웹소설(유료)'), ('free', '자유연재(무료)')]
GENRE_CHOICES = [('현대로맨스', '현대로맨스'), ('로맨스판타지', '로맨스판타지'), ('현대BL','현대BL'), ('판타지 BL', '판타지 BL'), ('시대물 BL', '시대물 BL'), ('현대판타지', '현대판타지'), ('클래식판타지', '클래식판타지'), ('무협', '무협'), ('퓨전', '퓨전'), ('게임판타지', '게임판타지'), ('스포츠', '스포츠'), ('패러디', '패러디'), ('GL', 'GL'), ('일반', '일반'), ('라이트노벨', '라이트노벨')]
TERM_CHOICES = [(1, '1일'), (7, '1주'), (30, '1개월'), (90, '3개월'), (180,'6개월')]
MONTH_CHOICES= [tuple([x,x]) for x in range(1,13)]
DAY_CHOICES= [tuple([x,x]) for x in range(1,32)]
INTEGER_CHOICES= [tuple([x,x]) for x in range(1,32)]

class optionForm(forms.Form):
	best = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=BEST_CHOICES)
	genre = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=GENRE_CHOICES)
	term = forms.ChoiceField(choices=TERM_CHOICES)