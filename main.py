from document_parser import DocumentParser
from document_tagger import DocumentTagger
import spacy
import sys

def main(document_filepath: str, organization_tags: str, en_model_name: str):
    nlp_model = spacy.load(name=en_model_name)  
    doc_parser = DocumentParser(document_filepath=document_filepath)
    doc_tagger = DocumentTagger(parser=doc_parser, 
                                organization_tags=[tag.strip().lower() for tag in organization_tags.split(',')],
                                nlp_model=nlp_model) 

    suggested_auto_tags = doc_tagger.fetch_autotags()
    for suggested_auto_tag in suggested_auto_tags:
        print(suggested_auto_tag)



if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])