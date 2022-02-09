# Generated by Django 2.2.16 on 2022-02-07 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0008_merge_20220206_2317'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='title',
            name='genre',
        ),
        migrations.AddField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(help_text='Выберите жанр', related_name='titles', to='reviews.Genre', verbose_name='Жанр'),
        ),
    ]