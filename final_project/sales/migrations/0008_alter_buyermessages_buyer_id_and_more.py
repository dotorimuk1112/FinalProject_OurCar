# Generated by Django 5.0.3 on 2024-04-23 03:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0007_buyermessages_accepted'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyermessages',
            name='buyer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buyer_messages', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='buyermessages',
            name='post_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_messages', to='sales.carsalespost'),
        ),
        migrations.AlterField(
            model_name='buyermessages',
            name='seller_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seller_messages', to=settings.AUTH_USER_MODEL),
        ),
    ]
