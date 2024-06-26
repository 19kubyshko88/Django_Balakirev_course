# Generated by Django 4.2.6 on 2024-01-24 05:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('itclub', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='studentarticles',
            name='author',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='studentarticles',
            name='cat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='itclub.category', verbose_name='Категории'),
        ),
        migrations.AddField(
            model_name='studentarticles',
            name='summary',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='related_post', to='itclub.summary', verbose_name='Резюме'),
        ),
        migrations.AddField(
            model_name='studentarticles',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='articles', to='itclub.tagpost', verbose_name='Тэги'),
        ),
        migrations.AddIndex(
            model_name='studentarticles',
            index=models.Index(fields=['-time_create'], name='itclub_stud_time_cr_ba4e23_idx'),
        ),
    ]
