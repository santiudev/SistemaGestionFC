# Generated by Django 5.1.1 on 2024-10-14 18:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finanzas', '0006_alter_mediopago_moneda'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediopago',
            name='moneda',
            field=models.CharField(choices=[('USD', 'Dólares'), ('PESOS', 'Pesos')], max_length=10),
        ),
    ]