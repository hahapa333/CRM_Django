from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db.models import Sum

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, View, DeleteView

from .admin_mixins import GroupRequiredMixin
from .form import ClientWithContractForm, ContractForm
from .models import Service, Campaign, Lead, Client, Contract


def permission_denied_view(request):
    return render(request, 'errors/permission_denied.html', status=403)


def home_view(request):
    if request.user.is_authenticated:
        groups = request.user.groups.values_list('name', flat=True)
        return render(request, 'crm/base.html', {
            'username': request.user.username,
            'groups': groups,
        })
    return render(request, 'crm/base.html')


# === Статистика по кампаниям ===
def campaign_stats_view(request):
    campaigns = Campaign.objects.all()

    stats = []
    for campaign in campaigns:
        leads = Lead.objects.filter(campaign=campaign)
        clients = Client.objects.filter(lead__campaign=campaign)
        contracts = Contract.objects.filter(client__lead__campaign=campaign)

        total_leads = leads.count()
        total_clients = clients.count()
        total_income = contracts.aggregate(total=Sum('amount'))['total'] or 0
        budget = campaign.budget or 1  # избегаем деления на 0
        roi = total_income / budget if budget else 0

        stats.append({
            'campaign': campaign,
            'total_leads': total_leads,
            'converted_clients': total_clients,
            'income': total_income,
            'budget': budget,
            'roi': round(roi, 2)
        })

    return render(request, 'crm/campaign_stats.html', {'stats': stats})


class AuthGroupRequiredMixin(LoginRequiredMixin, GroupRequiredMixin):
    pass


class ServiceListView(AuthGroupRequiredMixin, ListView):
    model = Service
    template_name = 'crm/service_list.html'


class ServiceCreateView(AuthGroupRequiredMixin, CreateView):
    model = Service
    fields = ['name', 'description', 'price']
    template_name = 'crm/form.html'
    success_url = reverse_lazy('service_list')


class ServiceUpdateView(AuthGroupRequiredMixin, UpdateView):
    model = Service
    fields = ['name', 'description', 'price']
    template_name = 'crm/form.html'
    success_url = reverse_lazy('service_list')


class CampaignListView(AuthGroupRequiredMixin, ListView, ):
    model = Campaign
    group_required = ['marketer']  # Можно список или строку
    template_name = 'crm/campaign_list.html'


class CampaignCreateView(AuthGroupRequiredMixin, CreateView):
    model = Campaign
    fields = ['name', 'service', 'promotion_channel', 'budget', 'start_date', 'end_date']
    template_name = 'crm/form.html'
    success_url = reverse_lazy('campaign_list')
    group_required = ['marketer']  # Можно список или строку

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание рекламной кампании'
        return context


class CampaignUpdateView(AuthGroupRequiredMixin, UpdateView):
    model = Campaign
    fields = ['name', 'start_date', 'end_date', 'budget']
    template_name = 'crm/form.html'
    group_required = ['marketer']  # Можно список или строку
    success_url = reverse_lazy('campaign_list')


class CampaignDeleteView(AuthGroupRequiredMixin, DeleteView, ):
    model = Campaign
    template_name = 'crm/campaign_confirm_delete.html'
    group_required = ['marketer']  # Можно список или строку
    success_url = reverse_lazy('campaign_list')


class CampaignDetailView(AuthGroupRequiredMixin, DetailView, ):
    model = Campaign
    group_required = ['marketer']  # Можно список или строку
    template_name = 'crm/campaign_detail.html'


class LeadListView(AuthGroupRequiredMixin, ListView):
    model = Lead
    group_required = ['operator', 'manager']  # Можно список или строку
    template_name = 'crm/lead_list.html'


class LeadCreateView(AuthGroupRequiredMixin, CreateView, ):
    model = Lead
    fields = ['name', 'email', 'phone', 'campaign']
    template_name = 'crm/form.html'
    group_required = ['operator']  # Можно список или строку
    success_url = reverse_lazy('lead_list')


class LeadUpdateView(AuthGroupRequiredMixin, UpdateView, ):
    model = Lead
    fields = ['name', 'email', 'phone', 'campaign', 'is_converted']
    template_name = 'crm/form.html'
    group_required = ['operator']  # Можно список или строку
    success_url = reverse_lazy('lead_list')


class ClientListView(AuthGroupRequiredMixin, ListView):
    model = Client
    template_name = 'crm/client_list.html'


class ClientCreateView(AuthGroupRequiredMixin, CreateView):
    model = Client
    fields = ['lead']
    template_name = 'crm/form.html'
    success_url = reverse_lazy('client_list')


class ClientWithContractCreateView(AuthGroupRequiredMixin, View):
    def get(self, request):
        initial_data = {}
        lead_id = request.GET.get('lead_id')
        if lead_id:
            initial_data['lead'] = lead_id
        form = ClientWithContractForm(initial=initial_data)
        return render(request, 'crm/form.html', {'form': form})

    def post(self, request):
        form = ClientWithContractForm(request.POST)
        if form.is_valid():
            lead = form.cleaned_data['lead']
            # ❗ Проверка существования клиента
            if Client.objects.filter(lead=lead).exists():
                messages.error(request, 'Клиент с этим лидом уже существует.')
                return redirect('lead_list')
            if lead.is_converted:
                messages.error(request, 'Клиент уже был сконвертирован.')
                return redirect('lead_list')

            lead.is_converted = True
            lead.save()
            client = Client.objects.create(lead=lead)
            Contract.objects.create(
                client=client,
                service=form.cleaned_data['service'],
                signed_date=form.cleaned_data['signed_date'],
                details=form.cleaned_data['details']
            )
            messages.success(request, 'Клиент и контракт успешно созданы!')
            return redirect('client_list')
        return render(request, 'crm/form.html', {'form': form})


class ClientDetailView(AuthGroupRequiredMixin, DetailView):
    model = Client
    template_name = 'crm/client_detail.html'


class ClientUpdateView(AuthGroupRequiredMixin, UpdateView):
    model = Client
    fields = ['lead']
    template_name = 'crm/form.html'
    success_url = reverse_lazy('client_list')


class ClientDeleteView(AuthGroupRequiredMixin, DeleteView):
    model = Client
    template_name = 'crm/client_confirm_delete.html'
    success_url = reverse_lazy('client_list')
    success_message = "Клиент успешно удалён."


class ContractListView(AuthGroupRequiredMixin, ListView, ):
    model = Contract
    group_required = ['manager']  # Можно список или строку
    template_name = 'crm/contract_list.html'


class ContractCreateView(AuthGroupRequiredMixin, CreateView, ):
    model = Contract
    form_class = ContractForm
    template_name = 'crm/contract_form.html'
    group_required = ['manager']  # Можно список или строку
    success_url = reverse_lazy('contract_list')


class ContractDetailView(AuthGroupRequiredMixin, DetailView, ):
    model = Contract
    template_name = 'crm/contract_detail.html'
    group_required = ['manager']  # Можно список или строку
    context_object_name = 'contract'


class ContractUpdateView(AuthGroupRequiredMixin, UpdateView, ):
    model = Contract
    form_class = ContractForm
    template_name = 'crm/contract_form.html'
    group_required = ['manager']  # Можно список или строку
    success_url = reverse_lazy('contract_list')


class ContractDeleteView(AuthGroupRequiredMixin, DeleteView, ):
    model = Contract
    template_name = 'crm/contract_confirm_delete.html'
    group_required = ['manager']  # Можно список или строку
    success_url = reverse_lazy('contract_list')
