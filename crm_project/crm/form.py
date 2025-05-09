from django import forms

from .models import Service, Campaign, Lead, Client, Contract





class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'description']

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = ['name', 'start_date', 'end_date', 'budget']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'email', 'phone', 'campaign', 'is_converted']

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['lead']


class ClientWithContractForm(forms.Form):
    lead = forms.ModelChoiceField(
        queryset=Lead.objects.filter(is_converted=False),
        label="Потенциальный клиент"
    )
    service = forms.ModelChoiceField(queryset=Service.objects.all(), label="Услуга")
    signed_date = forms.DateField(widget=forms.SelectDateWidget, label="Дата подписания")
    details = forms.CharField(widget=forms.Textarea, label="Детали контракта")

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['title', 'client', 'service', 'document', 'signed_date', 'valid_until', 'amount']
        widgets = {
            'signed_date': forms.DateInput(attrs={'type': 'date'}),
            'valid_until': forms.DateInput(attrs={'type': 'date'}),
        }
