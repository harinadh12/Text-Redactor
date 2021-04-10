The Redactor

Author :  Harinadh Appidi
This project has been implemented in python and can be run from command line with the below command.
pipenv run python redactor.py --input '*.txt' \
                    --names --dates --phones \
                    --concept 'court' \
                    --output 'files/' \
                    --stats stderr
 This project can be used to mask sensitive information in .txt and .md files.
All these files have to be present where the above pipenv command is run. 
For testing of this project some general information is taken from internet and enriched with some other info in a .txt file.
Packages used in this Project :
•	nltk
•	spacy
•	argparse
•	spacy
•	os
•	glob
•	phonenumbers
•	logging
•	en_core_web_sm

main.py
	This is the main file where the execution of the project starts.
In this file all the input arguments from command line are parsed and respective functions are called for further processing of txt files.
Below are the arguments that are parsed.
--input, --names, --gender, --date, --concept,  --output,  --stats
redactor.py
In this file, I have added different functions for all the functionalities (arguments in above step).

handle_input_files(files):
This method takes argument of –-input flag and extracts the data from all the .txt files in the working dir. 
	This data is returned back to the main file.
redact_names(input_data):
	This method is called when –-names flag is passed in the command line.
This method takes input data returned from handle_input_files() and mask names in the data with Unicode character ██ .
For this purpose, spacy & nltk libraries have been used to identify entities ‘PERSON, ‘GPE’ and ORGANIZATION as all of them are considered names and in particular proper nouns.
This method couldn’t identify some of the surnames or last names and some non-english (not native) names because of spacy and nltk limitations.
redact_dates(input_data):
	This method is called if –-dates flag is passed.
	It takes input data and returns the text with dates masked.
For this purpose, spacy library has been used to identify the labels with “DATE” tag and  also regex has been used to mask where month names are not identified by spacy.
redact_phones(input_data):
	This method is called if –-phones flag is passed.
	It takes input data and returns the text with phone numbers masked.
For this purpose, phonenumbers library has been used to identify the phone numbers.
Below is the github url for the phone numbers package that has been referred for this project. It has been used as it is a pure python project and multiple country phone numbers were handled .
https://github.com/daviddrysdale/python-phonenumbers

redact_gender(input_data):
	This method is called if –-genders flag is passed.
	It takes input data and returns the text with words that are related to gender masked.
Some gender related words are used as filter criteria along with pronoun tag of spacy library to mask gender words.
However, it doesn’t mask all gender words as identifying all of them is not possible through filter and requires higher order processing in natural language space.

redact_concept(input_data,concept):
	This method is called if –-concept flag is passed along with the concept.
	It takes input data and returns the text with words related to concept masked.
For this purpose, nltk wordnet synsets  has been used to find synonyms and related words relevant to the concept.
Though this could identify synonyms to some extent , there would equally or a greater number of cases where lot of relevant words are not identified because of library limitations.
Distance measurement libraries are not used as we are not comparing 2 sentences and it doesn’t yield much better result.
write_stats(stats_list):
This method is used to write the redaction type and number of words redacted in the txt document.
get_output(input_files,input_data,output_path):
	This method is used to write the output data after all the redaction steps into a .redacted file in the output path.
	A corresponding .redacted file w.r.t a input .txt file is written at the output path.

Test Cases
	test_redact_names.py
•	This method is used to test redact names functionality. It asserts true if at least 1 word is masked.
test_redact_phno.py
•	This method is used to test redact phone numbers functionality. It asserts true if at least 1 word (phno) is masked.
test_redact_gender.py
•	This method is used to test redact gender functionality. It asserts true if at least 1 word (gender relevant) is masked.
test_redact_dates.py
•	This method is used to test redact dates functionality. It asserts true if at least 1 word (date) is masked.
test_redact_concept.py
•	This method is used to test redact concepts functionality. It asserts true if at least 1 word (concept relevant) is masked.

To run test cases, navigate to the tests folder and run pipenv run python -m pytest
To run the project, navigate to project1 folder and run the below command.
	pipenv run python main.py --input '*.txt' --names --dates --phones --genders --concept 'court' --output 'files' --stats stderr.





