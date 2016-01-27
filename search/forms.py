from bootstrap3_datetime.widgets import DateTimePicker
from django import forms

class ToDoForm(forms.Form):
    Start_Date = forms.DateField(
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False}))
    End_Date = forms.DateTimeField(
        widget=DateTimePicker(options={"format": "YYYY-MM-DD",
                                       "pickTime": False}))
