from django import forms

districts = (
    ("1","চট্টগ্রাম"),
    ("2","কক্সবাজার"),
    ("3","বান্দরবান"),
    ("4","রাঙ্গামাটি"),
    ("5","খাগড়াছড়ি"),
)

categories = (
    ("1","সমুদ্র"),
    ("2","পাহাড়"),
    ("3","ঝর্ণা"),
    ("4","দ্বীপ"),
    ("5","লেক"),
    ("6","নদী"),
    ("7","বন"),
    ("8","পার্ক"),
)

class SearchForm(forms.Form):  
    source = forms.ChoiceField(choices = districts, label="Source", required=False)  
    destination  = forms.ChoiceField(choices = districts, label="Destination", required=False)
    date = forms.DateField(input_formats=['%d-%m-%Y'], required=False)
    day = forms.IntegerField(label="Day", max_value=50, required=False)
    budget = forms.IntegerField(label="Budget", required=False)
    category = forms.ChoiceField(choices = categories, label="Category", required=False)

