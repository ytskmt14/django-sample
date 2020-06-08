from django import forms
from .models import TopListModel, DetailListModel, SubDetailListModel, DetailWork

class TopForm(forms.ModelForm):
    title = forms.CharField(label='タイトル', max_length=50, required=True, widget=forms.TextInput())
    memo = forms.CharField(label='メモ', max_length=100, widget=forms.TextInput())
    date_from = forms.DateField(label='出発日', required=True, widget=forms.DateInput())
    date_to = forms.DateField(label='帰宅日', required=True, widget=forms.DateInput())
    images = forms.ImageField(label='イメージ画像', required=False)

    class Meta:
        model = TopListModel
        fields = ('title', 'memo', 'date_from', 'date_to', 'images')

class DetailForm(forms.ModelForm):
    date = forms.DateField(label='日付', required=True, widget=forms.DateInput())
    main_content = forms.CharField(label='やること', max_length=100, widget=forms.TextInput())

    class Meta:
        model = DetailListModel
        fields = ('date', 'main_content', 'top')

class SubDetailForm(forms.ModelForm):
    time = forms.TimeField(label='時間', required=True, widget=forms.TimeInput())
    main_content = forms.CharField(label='やること', max_length=100, widget=forms.TextInput())
    images = forms.ImageField(label='イメージ画像', required=False)
    hp_url = forms.URLField(label='ホームページのＵＲＬ', required=False,  widget=forms.TextInput())
    map_url = forms.URLField(label='地図のＵＲＬ', required=False,  widget=forms.TextInput())
    root_url = forms.URLField(label='経路のＵＲＬ', required=False,  widget=forms.TextInput())
    content1 = forms.CharField(label='メモ１', max_length=100, required=False,  widget=forms.TextInput())
    content2 = forms.CharField(label='メモ２', max_length=100, required=False,  widget=forms.TextInput())
    content3 = forms.CharField(label='メモ３', max_length=100, required=False,  widget=forms.TextInput())
    content4 = forms.CharField(label='メモ４', max_length=100, required=False,  widget=forms.TextInput())
    content5 = forms.CharField(label='メモ５', max_length=100, required=False,  widget=forms.TextInput())
    content6 = forms.CharField(label='メモ６', max_length=100, required=False,  widget=forms.TextInput())
    content7 = forms.CharField(label='メモ７', max_length=100, required=False,  widget=forms.TextInput())
    content8 = forms.CharField(label='メモ８', max_length=100, required=False,  widget=forms.TextInput())
    content9 = forms.CharField(label='メモ９', max_length=100, required=False,  widget=forms.TextInput())
    content10 = forms.CharField(label='メモ１０', max_length=100, required=False,  widget=forms.TextInput())

    class Meta:
        model = SubDetailListModel
        fields = ('time', 'main_content', 'images', 'hp_url', 'map_url', 'root_url', 'content1', 'content2', 'content3', 'content4', 'content5', 'content6', 'content7', 'content8', 'content9', 'content10', 'detail')

class DetailWorkForm(forms.ModelForm):
    date = forms.DateField(label='日付', required=True, widget=forms.DateInput())
    main_content = forms.CharField(label='やること', max_length=100, widget=forms.TextInput())

    class Meta:
        model = DetailWork
        fields = ('date', 'main_content')

class DetailIdForm(forms.Form):
    detail_id = forms.IntegerField()