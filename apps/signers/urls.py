from django.urls import path
from apps.signers.views import SignerListView, SignerDetailView

app_name = "signers"

urlpatterns = [
    path('document/<int:document_id>/', SignerListView.as_view(), name='signer_list'),
    path('<int:signer_id>/', SignerDetailView.as_view(), name='signer_detail'),
]
