# Generated by Django 5.0.1 on 2024-01-14 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_comment_body_alter_comment_stars'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='products/product_cover/', verbose_name='Product Image'),
        ),
    ]