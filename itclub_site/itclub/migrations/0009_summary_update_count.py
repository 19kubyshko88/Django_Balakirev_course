# Generated by Django 4.2.6 on 2023-12-07 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('itclub', '0008_summary_alter_studentarticles_tags_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='summary',
            name='update_count',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
