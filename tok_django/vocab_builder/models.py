# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class Document(models.Model):
	D_TYPE_CHOICES = (
		('book', 'book'),
		('webpage', 'webpage'),
		('news', 'news'),
		('other', 'other'),
	)
	url = models.CharField(max_length=200, blank=True)
	title = models.CharField(max_length=200, blank=True)
	d_type = models.CharField(max_length=50, choices=D_TYPE_CHOICES, blank=False, default='webpage')


class Sentence(models.Model):
	text = models.TextField(blank=True, null=False)
	doc = models.ForeignKey(Document, related_name='sents', null=False)


class Token(models.Model):
	T_TYPE_CHOICES = (
		('word', 'word'),
		('phrase', 'phrase'),
	)
	t_type = models.CharField(max_length=20, choices=T_TYPE_CHOICES, blank=False, default='word')
	d_freq = models.IntegerField(default=0)	# document frequency
	m_freq = models.IntegerField(default=0) # mention frequency
	r_freq = models.IntegerField(default=0) # review frequency
	i_freq = models.IntegerField(default=0) # internet frequency


class Meaning(models.Model):
	# The class to store a meaning of a word. Because a token may have multiple meanings
	# Optional for now
	token = models.ForeignKey(Token, related_name='meanings')

class Review(models.Model):
	# A review is an occurrence when user tries to remember a word
	token = models.ForeignKey(Token, related_name='reviews')
	doc = models.ForeignKey(Document, related_name='reviews', null=True)
	time = models.DateTimeField(auto_now_add=True)


class Mention(models.Model):
	token = models.ForeignKey(Token, related_name='mentions')
	sent = models.ForeignKey(Sentence, related_name='mentions')

