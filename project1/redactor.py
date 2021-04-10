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
#import en_core_web_sm
#nlp = en_core_web_sm.load()

stats_list = []

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
                string = "redact_names"
                get_stats(string,len(names_list))
                names_list.clear()

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
                    
                    dates_list.append(d.text)
            
            for date in dates_list:
                data = data.replace(date,"\u2588" * len(date))

            months = ['january','february','march','april','may','june','july','august','septmeber','november','december','jan','feb','mar','apr','jun','jul','aug','sep','oct','nov','dec']
            for m in months:
                replace_data = re.compile(re.escape(' ' + m + ' '), re.IGNORECASE)
                data = replace_data.sub("\u2588" * len(m),data)
            masked_data.append(data)
            
            string = "redact_dates"
            get_stats(string,len(dates_list))
            dates_list.clear()

    
        return masked_data
        
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
            
            string = "redact_phones"
            get_stats(string,len(phn_list))
            phn_list.clear()

        
        return mask_phns
            
            
    except Exception as error:
        LOGGER.exception("Exception in redact phones method")
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

            string = "redact_gender"
            #print("****************",gender_list)
            get_stats(string,len(gender_list))
            gender_list.clear()

            mask_genders.append(data)

        return mask_genders
    except Exception as error:
        LOGGER.exception("Exception in redact gender method")
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

        string = "redact_concept"
        get_stats(string, len(all_syns))
        
        
        return mask_data
                        
    except Exception as error:
        LOGGER.exception("Exception in redact concept method")
        raise error

def get_stats(redacted_type = None, count = 0):
    try:
    
        temp = "The word count of  " + redacted_type + " : " + str (count)
        stats_list.append(temp)
        
        return stats_list

    except Exception as error:
        LOGGER.exception("Exception in stats() method")
        raise error

def write_stats(stats_list=stats_list):
    try:
        path = ('./stderr/stderr.txt')
    
        file = open(path, "w", encoding="utf-8")
        for i in range(len(stats_list)):
            file.write(stats_list[i])
            file.write("\n")
        file.close()
        
        return stats_list

    except Exception as error:
        LOGGER.exception("Exception in write_stats method")
        raise error

def get_output(input_files,input_data,output_path):
    
    try:
        filenames =[]
        files = nltk.flatten(input_files)
        for i in range(len(files)):
            input_files = glob.glob(files[i])
        
            for j in range(len(input_files)):
                if '.txt' in  input_files[j]:
                    input_files[j] = input_files[j].replace(".txt", ".redacted")
                if '.md' in input_files[j]:
                    input_files[j] = input_files[j].replace(".md", ".redacted")
                if '\\' in input_files[j]:
                    input_files[j]= input_files[j].split("\\")
                    input_files[j] = input_files[j][1]
                
                filenames.append(input_files[j])

        for i in range(len(input_data)):
            for j in range(len(filenames)):
                if i==j:
                    file_data = input_data[i]
                    
                    path1 = (os.getcwd())
            
                    path2 = (output_path+'/'+filenames[j])
                    final_file = open(os.path.join(path1,path2), "w" ,encoding="utf-8")
                    
                    final_file.write(file_data)
                    final_file.close()
                    
        return len(filenames)

    except Exception as error:
        LOGGER.exception("Exception in write_stats method")
        raise error
