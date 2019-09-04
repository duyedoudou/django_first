# -*- coding: utf-8 -*-
from django import forms

class PdfExtractForm(forms.Form):
    file = forms.FileField()
    page = forms.CharField(max_length=30)

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file.name.lower().endswith('.pdf'):
            raise forms.ValidationError('zhiyunxuPDF.')
        return file


class PdfMergeForm(forms.Form):
    file1 = forms.FileField()
    file2 = forms.FileField(required=False)
    file3 = forms.FileField(required=False)
    file4 = forms.FileField(required=False)
    file5 = forms.FileField(required=False)


class PdfReplaceForm(forms.Form):
    file1 = forms.FileField()
    file2 = forms.FileField()
    page = forms.IntegerField()



