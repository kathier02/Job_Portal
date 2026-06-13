from django import forms
from .models import JobCategory, Company


class JobCategoryForm(forms.ModelForm):
    class Meta:
        model = JobCategory
        fields = '__all__'


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
