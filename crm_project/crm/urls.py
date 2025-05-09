from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views
from .views import ClientWithContractCreateView, permission_denied_view

urlpatterns = [

    path('', views.home_view, name='home'),
    path('campaigns/stats/', views.campaign_stats_view, name='campaign_stats'),
    path('permission-denied/', views.permission_denied_view, name='permission_denied'),
    path('services/', views.ServiceListView.as_view(), name='service_list'),
    path('services/new/', views.ServiceCreateView.as_view(), name='service_create'),
    path('services/<int:pk>/edit/', views.ServiceUpdateView.as_view(), name='service_edit'),

    path('campaigns/', views.CampaignListView.as_view(), name='campaign_list'),
    path('campaigns/new/', views.CampaignCreateView.as_view(), name='campaign_create'),
    path('campaigns/<int:pk>/edit/', views.CampaignUpdateView.as_view(), name='campaign_edit'),
    path('campaigns/<int:pk>/', views.CampaignDetailView.as_view(), name='campaign_detail'),
    path('campaigns/<int:pk>/delete/', views.CampaignDeleteView.as_view(), name='campaign_delete'),
    path('leads/', views.LeadListView.as_view(), name='lead_list'),
    path('leads/new/', views.LeadCreateView.as_view(), name='lead_create'),
    path('leads/<int:pk>/edit/', views.LeadUpdateView.as_view(), name='lead_edit'),

    path('clients/', views.ClientListView.as_view(), name='client_list'),
    path('clients/new/', views.ClientCreateView.as_view(), name='client_create'),
    path('clients/<int:pk>/', views.ClientDetailView.as_view(), name='client_detail'),
    path('clients/<int:pk>/edit/', views.ClientUpdateView.as_view(), name='client_edit'),
    path('clients/<int:pk>/delete/', views.ClientDeleteView.as_view(), name='client_delete'),
    path('clients/create_with_contract/',
         ClientWithContractCreateView.as_view(),
         name='client_with_contract_create'),
    path('contracts/', views.ContractListView.as_view(), name='contract_list'),
    path('contracts/new/', views.ContractCreateView.as_view(), name='contract_create'),
    path('contract/<int:pk>/', views.ContractDetailView.as_view(), name='contract_detail'),
    path('contracts/<int:pk>/edit/', views.ContractUpdateView.as_view(), name='contract_edit'),
    path('contracts/<int:pk>/delete/', views.ContractDeleteView.as_view(), name='contract_delete'),
    # path('register/', views.RegisterView.as_view(), name='register'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler403 = permission_denied_view
