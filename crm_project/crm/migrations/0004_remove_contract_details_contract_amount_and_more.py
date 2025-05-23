# Generated by Django 5.2 on 2025-05-07 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0003_campaign_promotion_channel_campaign_service'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contract',
            name='details',
        ),
        migrations.AddField(
            model_name='contract',
            name='amount',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contract',
            name='document',
            field=models.FileField(default=1, upload_to='contracts/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contract',
            name='title',
            field=models.CharField(default='Новый контракт', max_length=255),
        ),
        migrations.AddField(
            model_name='contract',
            name='valid_until',
            field=models.DateField(default='2025-05-07'),
            preserve_default=False,
        ),
    ]
