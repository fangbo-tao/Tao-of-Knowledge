# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Sentence(models.Model):
	text = models.TextField(blank=True, null=False)


class Token(models.Model):
	t_type = models.CharField(max_length=20)


class Document(models.Model):
	url = models.CharField(max_length=200)