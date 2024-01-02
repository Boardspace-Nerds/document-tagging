from document_parser import DocumentParser
from document_tagger import DocumentTagger
import spacy
import sys

def main(document_filepath: str, en_model_name: str):
    nlp_model = spacy.load(name=en_model_name)  
    doc_parser = DocumentParser(document_filepath=document_filepath)
    doc_tagger = DocumentTagger(parser=doc_parser, 
                                organization_tags=['porn', 'hentai', 'anime', 'machine learning', 'society', 'language', 'artificial intelligence', 'data', 'company'],
                                nlp_model=nlp_model) 

    print(doc_tagger.fetch_autotags())


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])