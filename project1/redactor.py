import nltk
import spacy
import re
import os
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('wordnet')
#from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk import ne_chunk
from nltk.corpus import stopwords
from nltk.corpus import wordnet

from nltk.tag.stanford import StanfordNERTagger

import glob
import nltk
import logging
import phonenumbers

LOGGER = logging.getLogger("REDACT_APP")

nlp = spacy.load('en_core_web_sm')

def handle_input_files(files):
    try:

        all_data = []
        all_files = nltk.flatten(files)
        for files in all_files:
            lst_fls = glob.glob(files)

            for each_file in lst_fls:
                data = open(each_file,"r").read()
                all_data.append(data)
           
        return all_data
    except Exception as error:
        LOGGER.exception("Exception in reading input files")
        raise error

def redact_names(input_data):
    try:
        if isinstance(input_data,list):
            names_list = []
            masked_data = []
            for data in input_data:          
                doc = nlp(data)

                for e in doc.ents:
                    if e.label_ in ["PERSON", "ORG", "GPE"]:
                       names_list.append(e.text)

                token_words = nltk.word_tokenize(data)
                pos_tags = nltk.pos_tag(token_words)

                named_entities = nltk.ne_chunk(pos_tags)
                
                for entities in named_entities.subtrees():
                    #print("**************entities**********",entities.label())
                    if entities.label() in [ "PERSON","GPE", "ORGANIZATION"]:
                        for l in entities.leaves():
                            if l[0] not in names_list:
                                names_list.append(l[0])
                #print("******** Named Entities **************",names_list)
                for name in names_list:
                    data = data.replace(name,"\u2588" * len(name))
                masked_data.append(data)
            #print("*****************",masked_data)
            return masked_data

    except Exception as error:
        LOGGER.exception("Exception in redact names method")
        raise error


def redact_dates(input_data):
    try:
        from date_extractor import extract_dates
        dates_list = []
        masked_data = []
        for data in input_data:
            doc = nlp(data)
            for d in doc.ents:
                if d.label_ == "DATE" and len(d.text) > 2:
                    #print(d.text,d.label_)
                    dates_list.append(d.text)
            #print("**********dates list*************",dates_list)
            for date in dates_list:
                data = data.replace(date,"\u2588" * len(date))

            months = ['january','february','march','april','may','june','july','august','septmeber','november','december','jan','feb','mar','apr','jun','jul','aug','sep','oct','nov','dec']
            for m in months:
                replace_data = re.compile(re.escape(' ' + m + ' '), re.IGNORECASE)
                data = replace_data.sub("\u2588" * len(m),data)
            masked_data.append(data)
        
        print("".join(masked_data))
        return masked_data

        #dates_list = []
        #for data in input_data:
            #dates = extract_dates(data)
            #print(dates)

    except Exception as error:
        LOGGER.exception("Exception in redact names method")
        raise error

def redact_phones(input_data):
    try:
        phn_list = []
        mask_phns = []
        for data in input_data:
            phnos = phonenumbers.PhoneNumberMatcher(data,"US")
            for match in phnos:
                phn_list.append(str(match.number.national_number))
        
            for phn in phn_list:
                data = data.replace(phn,"\u2588" * len(phn))
            mask_phns.append(data)
        print(mask_phns)

        return mask_phns
            
            
    except Exception as error:
        LOGGER.exception("Exception in redact names method")
        raise error

def redact_gender(input_data):
    
    try:
        gender_list = []
        mask_genders = []
        gender_filter = ['male','female','wife','husband','king','queen','feminine','masculine','father','brother','brother-in-law','sister','girl','boy','man','woman','women','men','actress','waitress','daughter','son','bride','groom','uncle','aunt','mom','mother','papa','niece','nephew']

        for data in input_data:
            doc = nlp(data)
            for token in doc:
                if token.pos_ == 'PRON':
                    gender_list.append(str(token))
            data_lst = data.split()
        
            for d in data_lst:
                for g in gender_filter:
                    if g in d.lower():
                        gender_list.append(d)
            
            for g in gender_list:
                data = data.replace( g + ' ',"\u2588" * len(g))
            mask_genders.append(data)

    except Exception as error:
        LOGGER.exception("Exception in redact genders method")
        raise error

def redact_concept(input_data,concepts):
    try:
        synonyms = []
        synonyms_list = []
        for concept in concepts:
            for syn in wordnet.synsets(concept):
                synonyms.append(syn.lemma_names())
                for lemma in syn.hyponyms():
                    synm = lemma.lemma_names()
                    synonyms_list.append(synm)

        all_syns = list(nltk.flatten(synonyms_list))
        for i in concepts:
            all_syns.append(i)
        
        mask_data = []
        for data in input_data:
            doc = nlp(data)
            for sents in doc.sents:
                for concept in all_syns:
                    if concept in str(sents):
                        data = data.replace(str(sents),u"\u2588"*len(str(sents)))
            
            mask_data.append(data)
        
        return mask_data
                        
    except Exception as error:
        LOGGER.exception("Exception in redact concepts method")
        raise error
