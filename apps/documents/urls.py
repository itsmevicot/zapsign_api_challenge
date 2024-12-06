from django.urls import path
from apps.documents.views import DocumentListView, DocumentDetailView

app_name = 'documents'

urlpatterns = [
    path('', DocumentListView.as_view(), name='document_list'),
    path('<int:document_id>/', DocumentDetailView.as_view(), name='document_detail'),
]
