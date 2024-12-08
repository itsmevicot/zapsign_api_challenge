from django.db import models


class Signer(models.Model):
    token = models.CharField(max_length=255, null=True)
    status = models.CharField(max_length=50, null=True)
    name = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, null=False)
    external_id = models.CharField(max_length=255, null=True, blank=True)
    document = models.ForeignKey("documents.Document", on_delete=models.CASCADE, related_name='signers')

    class Meta:
        verbose_name = "Signer"
        verbose_name_plural = "Signers"

    def __str__(self):
        return self.name
