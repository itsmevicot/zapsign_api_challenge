# Generated by Django 5.1.3 on 2024-12-08 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('signers', '0002_alter_signer_document'),
    ]

    operations = [
        migrations.AlterField(
            model_name='signer',
            name='status',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='signer',
            name='token',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
