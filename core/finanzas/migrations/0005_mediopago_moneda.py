# Generated by Django 5.1.1 on 2024-10-14 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0004_alter_cotizaciondolar_fecha'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediopago',
            name='moneda',
            field=models.CharField(choices=[('USD', 'Dólares'), ('PESOS', 'Pesos')], default=2, max_length=10),
            preserve_default=False,
        ),
    ]
