# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-10 21:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vocab_builder', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meaning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Mention',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='document',
            name='d_type',
            field=models.CharField(choices=[('book', 'book'), ('webpage', 'webpage'), ('news', 'news'), ('other', 'other')], default='webpage', max_length=50),
        ),
        migrations.AddField(
            model_name='document',
            name='title',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AddField(
            model_name='sentence',
            name='doc',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='sents', to='vocab_builder.Document'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='token',
            name='d_freq',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='token',
            name='i_freq',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='token',
            name='m_freq',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='token',
            name='r_freq',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='document',
            name='url',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='token',
            name='t_type',
            field=models.CharField(choices=[('word', 'word'), ('phrase', 'phrase')], default='word', max_length=20),
        ),
        migrations.AddField(
            model_name='review',
            name='doc',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='vocab_builder.Document'),
        ),
        migrations.AddField(
            model_name='review',
            name='token',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='vocab_builder.Token'),
        ),
        migrations.AddField(
            model_name='mention',
            name='sent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mentions', to='vocab_builder.Sentence'),
        ),
        migrations.AddField(
            model_name='mention',
            name='token',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mentions', to='vocab_builder.Token'),
        ),
        migrations.AddField(
            model_name='meaning',
            name='token',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='meanings', to='vocab_builder.Token'),
        ),
    ]
