# -*- coding: utf-8 -*-
import sys
import os
import re
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

import django
django.setup()

import LDAmodel # import lda_parts, News, get_words
import gensim

 



def get_data():
    from feedreader.models import Entry
    Entrys = Entry.objects.all()
    n = len(Entrys)
    PKs = [Entrys[i].pk for i in range(n)]
    #Links = [Entrys[i].link for i in range(n)]
    
    p = re.compile(r"<[^>]*?>")

    Titles = [p.sub("", Entrys[i].title) for i in range(n)]

    Descriptions = [p.sub("", Entrys[i].description) for i in range(n)]

    return [PKs, Titles, Descriptions]






if __name__ == '__main__':
    argvs = sys.argv
    [PKs, Titles, Descriptions] = get_data()

    filters = True
    show = False
    num_topics = 20

    if sys.argv[1] == 'initial':

        title_lda  =  LDAmodel.lda_parts(Titles)
        title_lda.dictionary_corpus(filter = filters,show = show,save  =  ("./model/titles.dictionary"))#, no_below = no_below, no_above = no_above)
        print "dictionary of title made"

        title_lda.LDA_model(num_topics = num_topics,save = ("./model/titles.model"),show = show,set_matrix = False)
        print "LDA of title made"

        description_lda  =  LDAmodel.lda_parts(Descriptions)
        description_lda.dictionary_corpus(filter = filters,show = show, save  =  ("./model/descriptions.dictionary"))#, no_below = no_below, no_above = no_above)
        print "dictionary of description made"
        description_lda.LDA_model(num_topics = num_topics,save = ("./model/descriptions.model"),show = show,set_matrix = False)
        print "LDA of description made"


    NewsEntry = LDAmodel.News(PKs, Titles ,Descriptions, filters = True,show=False)
    Entrys = Entry.objects.all()

    for entry in Entrys:
        Revelant = NewsEntry.predictRelavent(entry.title, entry.description)
        if entry.id in  Revelant:
            Revelant.remove(entry.id)
        elif len(Revelant) == 4:
            Revelant=Revelant[:3]


        if len(Revelant) == 1:
            FisrtRevelant = Entry.objects.get(pk=Revelant[0])
        elif len(Revelant) == 2:
            FisrtRevelant = Entry.objects.get(pk=Revelant[0])
            SecondRevelant = Entry.objects.get(pk=Revelant[1])
        elif len(Revelant) == 3:
            FisrtRevelant = Entry.objects.get(pk=Revelant[0])
            SecondRevelant = Entry.objects.get(pk=Revelant[1])
            ThirdRevelant = Entry.objects.get(pk=Revelant[2])

        entry.save()


            

