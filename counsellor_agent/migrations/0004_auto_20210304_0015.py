# Generated by Django 3.1.7 on 2021-03-03 18:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('counsellor_agent', '0003_agentnotification'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentnotification',
            name='agency',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='agency', to='accounts.useraccounts'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='agentnotification',
            name='counsellor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='counsellor', to=settings.AUTH_USER_MODEL),
        ),
    ]
