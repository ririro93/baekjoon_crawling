# Generated by Django 3.1.5 on 2021-02-11 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('show_crawl_info', '0007_auto_20210205_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_number',
            field=models.CharField(default='번호 넣어줘..', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='question_title',
            field=models.CharField(default='제목 넣어줘..', max_length=200),
        ),
    ]
