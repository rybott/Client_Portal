# forms.py

from django import forms
from .models import Case, Company, Lawyer, LawFirm, Task

class CaseIntakeForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = [
            'summary',
            'short_name',
            'case_number',
            'case_type',
            'date_of_case',
            'plaintiff',
            'defendant',
            'hired_by',
            'stage',
        ]
        exclude = ['plaintiff_lawyer', 'defense_lawyer']
        widgets = {
            'date_of_case': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Optional: Use autocomplete-like widget (can later wire to JS or HTMX)
        self.fields['plaintiff'].queryset = Company.objects.order_by('name')
        self.fields['defendant'].queryset = Company.objects.order_by('name')

        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})  # Tailwind will override this anyway


class LawyerInlineForm(forms.ModelForm):
    law_firm_name = forms.CharField(
        max_length=255,
        required=False,
        help_text="Start typing to select or enter a new law firm."
    )

    class Meta:
        model = Lawyer
        fields = ['name', 'title']

    def save(self, commit=True):
        lawyer = super().save(commit=False)

        # Handle the law firm
        firm_name = self.cleaned_data.get('law_firm_name')
        if firm_name:
            law_firm, created = LawFirm.objects.get_or_create(name=firm_name)
            lawyer.law_firm = law_firm

        if commit:
            lawyer.save()
        return lawyer


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["task_type", "summary", "start_time", "end_time", "status"]
        widgets = {
            "summary": forms.Textarea(attrs={"rows": 3, "class": "w-full border rounded p-2"}),
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "w-full border rounded p-2"}),
            "end_time": forms.DateTimeInput(attrs={"type": "datetime-local", "class": "w-full border rounded p-2"}),
            "task_type": forms.TextInput(attrs={"class": "w-full border rounded p-2"}),
            "status": forms.Select(attrs={"class": "w-full border rounded p-2"}),
        }