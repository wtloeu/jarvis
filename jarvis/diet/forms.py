from django import forms
from .models import Entry, Food

class AddEntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['entry_date', 'food', 'servings']

    # Style forms for bootstrap
    def __init__(self, *args, **kwargs):
        super(AddEntryForm, self).__init__(*args, **kwargs)
        self.fields['entry_date'].widget.attrs.update({'class': 'form-control'})
        self.fields['food'].widget.attrs.update({'class': 'custom-select'})
        self.fields['food'].widget.attrs.update({'id': 'select-food'})
        self.fields['food'].queryset = self.fields['food'].queryset.order_by('name')

        self.fields['servings'].widget.attrs.update({'class': 'form-control', 'id': 'entry_amount_input'})
        self.fields['servings'].label = 'Amount:'

class AddFoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(AddFoodForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

        self.fields['name'].widget.attrs.update({'oninput': 'selectedFoodFromDatalist()', 'list': 'foods-datalist', 'id': 'fatsecret-search'})
        self.fields['serving_size'].widget.attrs.update({'class': 'custom-select', 'id': 'fatsecret-serving-size'})

class DeleteEntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ()

class UpdateFoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(UpdateFoodForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
