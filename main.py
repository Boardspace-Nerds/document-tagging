from document_parser import DocumentParser
from document_tagger import DocumentTagger
import spacy
import sys
import warnings


def main(document_filepath: str, organization_tags: str, en_model_name: str):
    nlp_model = spacy.load(name=en_model_name)  
    doc_parser = DocumentParser(document_filepath=document_filepath)
    doc_tagger = DocumentTagger(parser=doc_parser, 
                                organization_tags=[tag.strip().lower() for tag in organization_tags.split(',')],
                                nlp_model=nlp_model) 

    best_autotags, other_autotag_suggestions = doc_tagger.fetch_autotags()
    print(f'Best matching autotags from your required organizational tags list:\n{", ".join(best_autotags)}\n')
    print(f'Other automatic autotag suggestions that you might want to consider:\n{", ".join(other_autotag_suggestions)}\n')


if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    main(sys.argv[1], sys.argv[2], sys.argv[3])