#-*- coding: utf8 -*-

try:
	import os
	import pymongo
	import nltk
	from pickle import dump, load
except Exception as e:
	raise e


class cLing(object):

	def __init__(self):

		stop = self.tokenitza('La mare que et va matricular després')
		print stop
		
		# Try to load the taggers. 
		try:
			self.load_tagger('cess_ca_unigram.tagger').tag(['hola'])
		
		#If it not work create them
		#Això hauria destar a l'instalador
		except IOError:
			print "*** First-time use of cess tagger ***"
			print "Training tagger ..."
			from nltk.corpus import cess_cat as cess
			
			cess_words = cess.tagged_words()
			self.train_tagger('cess_ca',cess_words)

			print "\nTagger trained\n"
		
		tags = self.tagger_cess_ca(stop)
		print tags
		### TODO: Work with TrigramTagger ###
		### TODO: Set backoffs for every tagger ###





	def getStopWords(self, lang):
		stopwords = []
		with open('stopwords_'+lang+'.txt') as stopwordsfile:
			for line in stopwordsfile:
				stopwords.append(line.strip())
		return stopwords

	def elStopWords(self, word_list, lang):

		filtered_words = [word for word in word_list if word not in self.getStopWords(lang)]

		return filtered_words

	def tokenitza(self, string):
		tokens = nltk.word_tokenize(string)
		return tokens

	def load_tagger(self, tagger_file_name):

		with open(tagger_file_name, 'rb') as infile:
			tagger = load(infile)
		return tagger
	
		# Function to save tagger
	def savetagger(self, tagger_file_name, tagger):
		with open(tagger_file_name, 'wb') as outfile:
				dump(tagger, outfile, -1)

	def train_tagger(self, corpus_name, corpus):
			
		# Training UnigramTagger
		tagger1 = nltk.UnigramTagger(corpus)
		self.savetagger(corpus_name+'_unigram.tagger', tagger1)
		print "UnigramTagger trained with", corpus_name

	def tagger_cess_ca(self, words):
		self.uni = self.load_tagger('cess_ca_unigram.tagger')
		tags = self.uni.tag(words)
		return tags
		

cLing()