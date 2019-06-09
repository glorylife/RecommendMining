from django import forms


class StudentForm(forms.Form):
    StudentID = forms.CharField()
