from django import forms
from .models import UserData, KategoriaDanychWrazliwych, WyboryJurysdykcji

class UserDataForm(forms.ModelForm):
    typ_danych = forms.MultipleChoiceField(
        choices=KategoriaDanychWrazliwych.choices,
        widget=forms.CheckboxSelectMultiple,
        help_text="Wybierz wszystkie typy danych, które przetwarzasz."
    )
    class Meta:
        model = UserData
        fields = ['typ_danych', 'sektor', 'jurysdykcja', 'opis']
        help_texts = {
            'sektor': "Podaj sektor działalnosci, np. 'medyczny', 'finansowy'.",
            'jurysdykcja': "Wybierz jurysdykcję prawną, np. 'RODO', 'GDPR', 'CCPA'.",
            'opis': "Wprowadź opis danych."
        }
