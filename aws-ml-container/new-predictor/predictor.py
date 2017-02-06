import time
import socket
import urllib
#from pattern.web import Newsfeed
#from pattern.web import cache
from pattern.en import parse, pprint, tag
#from pattern.web import download, plaintext
import numpy as np
import nltk
import pickle
import random
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.cluster import KMeans
from gensim import corpora, models, similarities

def read_config_from_local(subj, basepath):
	docpath = "/config_"+subj+".json"
	with open(docpath, 'rb') as f:
		doc = f.read()
	z =json.loads(doc)
	subject = z['subject']
	loadset = z['loadset']
	subtopics = []
	for w in z['supertopics']:
		subtopics.extend([(w[0], w[1])])
	return subject, loadset, subtopics

def load_docs(path, name):
	filename = path+name+".p"
	fileobj = open(filename, "rb")
	z = fileobj.read()
	lst = pickle.loads(str(z))
	titles = []
	sitenames = []
	abstracts = []
	for i in range(0, len(lst)):
		titles.extend([lst[i][0]])
		sitenames.extend([lst[i][1]])
		abstracts.extend([lst[i][2]])
	   
	print("done loading "+filename)
	return abstracts, sitenames, titles


def load_data2(readtopics):
	titles, sitenames, disp_title = load_docs("/", "sciml_data_arxiv")
	print("len of titles, sitenames, disp_title")
	print( len(titles), len(sitenames), len(disp_title))
	return titles, sitenames, disp_title

def makeInvertedTrainingList(super_topics):
	#create list of all training set items
	#  (doc, docno, subtopicname, subtopic-index)
	lis = []
	n = 0
	for top in super_topics:
		items = top[1]
		for i in range(0, len(items)):
			lis.extend([(items[i], top[0], n)])
		n = n+1
	return lis

def findTopic(topdict, groupnames, found):
	for nm in groupnames:
		if topdict[nm].find(found)> 0:
			return nm
	return "none"
def maketopdic(supertopics):
	dic = {}
	for top in supertopics:
		items = top[1]
		s = ''
		for i in range(0, len(items)):
			s = s + ' '+items[i]
		dic[top[0]] = s
	return dic

def init_from_local(subj, basepath):
   
	basepath = ''
	subject, loadset, supertopics =read_config_from_local(subj, basepath)
	cvectpath = basepath+"/count_vectorizer-"+subject+".p"
	tfidftranpath = basepath+"/tfidf_transformer-"+subject+".p"
	rfpath = basepath+"/random_forest-"+subject+".p"
	namspath = basepath+"/supertopic_names-"+subject+".p"
	GBpath = basepath+"/gradientboosting-"+subject+".p"
	vectpath = basepath+"/vectorizer-"+subject+".p"
	lsimodpath = basepath+"/lsimod-"+subject+".p"
	lsiindpath = basepath+"/lsiind-"+subject+".p"
	ldamodpath = basepath+"/ldamod-"+subject+".p"
	ldaindpath = basepath+"/ldaind-"+subject+".p"
	kmpath =  basepath+"/km-"+subject+".p"
	ncentpath = basepath+"/ncent-"+subject+".p"
	Xpath = basepath+"/Xtrain-"+subject+".p"
	trainsetpath = basepath+"/Tset-"+subject+".p"
	dictpath = basepath+"/Dict-"+subject+".p"

	with open(cvectpath, 'rb') as f:
	   cvecb = f.read()
	with open(vectpath, 'rb') as f:
	   vecb = f.read()
	with open(tfidftranpath, 'rb') as f:
	   tranb = f.read()
	with open(namspath, 'rb') as f:
	   groupb = f.read()
	with open(rfpath, 'rb') as f:
	   rfbb = f.read()
	with open(lsimodpath, 'rb') as f:
	   lsimodb = f.read()
	with open(lsiindpath, 'rb') as f:
	   lsib = f.read()
	with open(ldamodpath, 'rb') as f:
	   ldamodb = f.read()
	with open(ldaindpath, 'rb') as f:
	   ldab = f.read()
	with open(kmpath, 'rb') as f:
	   kmpathb = f.read()
	with open(ncentpath, 'rb') as f:
	   ncentb = f.read()
	with open(Xpath, 'rb') as f:
	   Xb = f.read()
	with open(trainsetpath, 'rb') as f:
	   trainingb = f.read()
	with open(dictpath, 'rb') as f:
	   dictb = f.read()
  

	c_vectorizer = pickle.loads(str(cvecb))
	tfidf_transformer = pickle.loads(str(tranb))
	groupnames = pickle.loads(str(groupb))
	clfrf = pickle.loads(str(rfbb))
	vectorizer = pickle.loads(str(vecb))
	new_centroids = pickle.loads(str(ncentb))
	index_lsi = pickle.loads(str(lsib))
	lsi = pickle.loads(str(lsimodb))
	index_lda = pickle.loads(str(ldab))
	lda = pickle.loads(str(ldamodb))
	km = pickle.loads(str(kmpathb))
	Xtrain = pickle.loads(str(Xb))
	trainingSets = pickle.loads(str(trainingb))
	dictionary = pickle.loads(str(dictb))

	traininglist = makeInvertedTrainingList(trainingSets)
	traindocs = [tex[0] for tex in traininglist]
	trainlabel = [tex[1] for tex in traininglist]
	traintarget = [tex[2] for tex in traininglist]

	return  km, vectorizer, lsi, dictionary, index_lsi, lda, index_lda, Xtrain, traindocs, c_vectorizer, clfrf, tfidf_transformer, new_centroids, trainlabel, groupnames

#for an item in the titles list compare its nonlist vector to the list of centroid and return
#the sorted list (closest first)
def cosdist(vectorizer, itemno, centroids, nounlist):
	new_title_vec = vectorizer.transform([nounlist[itemno]])
	#new_title_vec = vectorizer.transform([titles[itemno]])
	scores = []
	for i in range(0, len(centroids)):
		dist = np.dot(new_title_vec.toarray()[0], centroids[i].toarray()[0])
		scores.extend([(dist, i)])
	scores = sorted(scores,reverse=True)
	return scores

#this version works for an arbitrary text string
def cosdistString(vectorizer, item, centroids):
	new_title_vec = vectorizer.transform([item])
	scores = []
	for i in range(0, len(centroids)):
		dist = np.dot(new_title_vec.toarray()[0], centroids[i].toarray()[0])
		scores.extend([(dist, i)])
	scores = sorted(scores,reverse=True)
	return scores

#returns list of tuples (distance, sitename, itemno, abstract for item)
def compdist(new_title_vec, indexlist, X, titles):
	similar = []
	for i in indexlist:
		if np.linalg.norm(X[i].toarray()) != 0.0:
			#dist = np.linalg.norm((new_title_vec-X[i]).toarray())
			dist = np.dot(new_title_vec.toarray()[0],X[i].toarray()[0])
			similar.append((dist,i, titles[i]))
	similar = sorted(similar,reverse=True)
	return similar

def clean(doc):
	st = ""
	sciencestopwords = set([u'model','according', 'data', u'models', 'function', 'properties', 'approach', 'parameters',
				'systems', 'number', 'order', u'data', 'analysis', u'information', u'journal',
				'results','using','research', 'consumers', 'scientists', 'model', 'models', 'journal',
				'researchers','paper','new','study','time','case', 'simulation', u'simulation', 'equation',
				'based','years','better', 'theory', 'particular','many','due','much','set', 'studies', 'systems',
				'simple', 'example','work','non','experiments', 'large', 'small', 'experiment', u'experiments',
				'provide', 'analysis', 'problem', 'method', 'used', 'methods'])
	for (word, pos) in tag(doc):
		if pos in ["JJ", "NNS", "NN", "NNP"]:
			st = st+word+" "
		else:
			if st!= "":
				st = st[0:-1]+" "
				#print "got one"
	wordl = st.lower().split()
	s = ""
	for word in wordl:
		if word not in sciencestopwords:
			s = s+" "+word
	return s

#the X and titles used here should be for the training list
def makeguess(statmt, km, vectorizer, lsi, dictionary, index_lsi, ldamodel, index_lda, X, titles):
	statement = clean(statmt)
	new_title_vec = vectorizer.transform([statement])
	new_title_label = km.predict(new_title_vec)
	similar_indicies = (km.labels_==new_title_label).nonzero()[0]
	similar = compdist(new_title_vec, similar_indicies, X, titles)
	kmeans_items = list(x[1] for x in similar)

	#now for lsi items
	new_title_vec_lsi = dictionary.doc2bow(statement.lower().split())
	new_title_lsi = lsi[new_title_vec_lsi]
	sims = index_lsi[new_title_lsi] # perform a similarity query against the corpus
	simlist = list(enumerate(sims))
	topten = sorted(simlist, key = lambda x: x[1], reverse = True)[0:30]
	lsi_items = list(x[0] for x in topten)

	#now do lda
	#new_title_vec_lda = dictionary.doc2bow(statement.lower().split())
	#new_title_lda = ldamodel[new_title_vec_lda]
	#sims = index_lda[new_title_lda] # perform a similarity query against the corpus
	#simlist = list(enumerate(sims))
	#topten = sorted(simlist, key = lambda x: x[1], reverse = True)[0:30]
	#lda_items = list(x[0] for x in topten)
	lda_items = lsi_items

   
	dist_lsi = compdist(new_title_vec, lsi_items, X, titles)
	dist_km = compdist(new_title_vec, kmeans_items, X, titles)
	dist_lda = compdist(new_title_vec, lda_items, X, titles)
	s = dist_lda + dist_km + dist_lsi
	d1 = sorted(s, reverse=True)
	d = [x for x in d1 if x[0] > 0.00]

	notdups = []
	for x in d:
		if x not in notdups:
			notdups.extend([x])
	return notdups

def bigpredict(statement, km, vectorizer, lsi, dictionary, index_lsi, lda, index_lda,
			   Xtrain, traindocs, c_vectorizer, clfrf, tfidf_transformer, new_centroids, trainlabel, groupnames ):
   
	bestof3l = makeguess(statement, km, vectorizer, lsi, dictionary, index_lsi,
						lda, index_lda, Xtrain, traindocs)
	if len(bestof3l)> 0:
		best = trainlabel[bestof3l[0][1]]
	else:
		best = "?"
	if len(bestof3l) > 1:
		nextb = trainlabel[bestof3l[1][1]]
	else:
		nextb = "?"
   
	X_new_counts = c_vectorizer.transform([statement])
	X_new_tfidf = tfidf_transformer.transform(X_new_counts)
	predictedrf = clfrf.predict(X_new_tfidf)
	rf = groupnames[predictedrf[0]]
   
	z = cosdistString(vectorizer, statement, new_centroids)
	if z[0][0] > 0.06:
		cent = groupnames[z[0][1]]
	else:
		cent = "??"
   
	return rf, best, nextb, cent

base = "/"
#ignoring the basepath param passed in
subj = "all4"
subject, loadset, supertopics =read_config_from_local(subj, base)
topdict = maketopdic(supertopics)
#titles, sitenames, disp_title = load_data2(loadset)
basepath = base
km, vectorizer, lsi, dictionary, index_lsi, lda, index_lda, Xtrain, traindocs, c_vectorizer, clfrf, tfidf_transformer, new_centroids, trainlabel, groupnames = init_from_local(subj, basepath)

class predictor:
	def __init__(self):
		print("init done")
	def predict(self, statmt, ans):
		statement = clean(statmt)
		rf, best, nextb, cent = bigpredict(statement, km, vectorizer, lsi, dictionary, index_lsi,
		lda, index_lda, Xtrain, traindocs, c_vectorizer, clfrf, tfidf_transformer, new_centroids,
										   trainlabel, groupnames )
		truval = findTopic(topdict, groupnames, ans)
		return rf, best, nextb, cent, truval




#d = 333
#print predict(d)
#print "correct = "+sitenames[d] 
#print ".........................................."
#d = 444
#print predict(d)
#print "correct = "+sitenames[d] 
