from django.urls import path
from apps.companies.views import CompanyListView, CompanyDetailView

app_name = "companies"


urlpatterns = [
    path('', CompanyListView.as_view(), name='company_list'),
    path('<int:company_id>/', CompanyDetailView.as_view(), name='company_detail'),
]
