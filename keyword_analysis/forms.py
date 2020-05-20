from django import forms


PLATFORM_CHOICES = [('all', '전체'), ('joara', '조아라'), ('monpia', '문피아'), ('bookfal', '북팔') ]
GENRE_CHOICES = [('all', '전체'), ('pantazy', '판타지'), ('romance', '로맨스'), ('BL','BL')]
TERM_CHOICES = [('day', '1일'), ('week', '1주'), ('_1month', '1개월'), ('_3month', '3개월'), ('_6month','6개월')]
MONTH_CHOICES= [tuple([x,x]) for x in range(1,13)]
DAY_CHOICES= [tuple([x,x]) for x in range(1,32)]
INTEGER_CHOICES= [tuple([x,x]) for x in range(1,32)]

class UserForm(forms.Form):
    first_name= forms.CharField(max_length=100)
    last_name= forms.CharField(max_length=100)
    email= forms.EmailField()
    age= forms.IntegerField()
    todays_date= forms.IntegerField(label="What is today's date?", widget=forms.Select(choices=INTEGER_CHOICES))
    #todays_date= forms.IntegerField(label="What is today's date?", widget=forms.Select(choices=INTEGER_CHOICES))

class optionForm(forms.Form):
    platform= forms.CharField(max_length=10, widget=forms.Select(choices=PLATFORM_CHOICES))
    genre = forms.CharField(max_length=10, widget=forms.Select(choices=GENRE_CHOICES))
    term = forms.CharField(max_length=5, widget=forms.Select(choices=TERM_CHOICES))