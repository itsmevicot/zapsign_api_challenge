from django.db import models


class Document(models.Model):
    open_id = models.IntegerField(null=False)
    token = models.CharField(max_length=255, null=False)
    name = models.CharField(max_length=255, null=False)
    status = models.CharField(max_length=50, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    created_by = models.CharField(max_length=255, null=False)
    company = models.ForeignKey("companies.Company", on_delete=models.PROTECT, related_name='documents')
    external_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"

    def __str__(self):
        return self.name
