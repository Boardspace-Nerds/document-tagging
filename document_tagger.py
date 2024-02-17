import random
from re import I
from typing import List, Dict, Set, Union, Tuple
from document_parser import DocumentParser
from spacy import Language
from spacy.tokens import Token

ExtractedTokenMap = Dict[int, Set[str]]

IMPORTANT_PARTS_OF_SPEECH: List[str] = ['NOUN', 'PROPN', 'ADJ']

class DocumentTagger:   
    parser: DocumentParser
    organization_tags: List[str]
    nlp_model: Language
    similarity_threshold: float

    def __init__(self, parser: DocumentParser, organization_tags: List[str], nlp_model: Language, similarity_threshold: float = 0.80):
        self.parser = parser
        self.nlp_model = nlp_model 
        self.similarity_threshold = similarity_threshold
        self.organization_tags = self._normalize_organization_tags(organization_tags)     
        self.organization_tag_mapping = {organization_token : organization_tag for organization_token, organization_tag in zip(self.organization_tags, organization_tags) }     
        self.extracted_token_map: Union[ExtractedTokenMap, None] = None

    def _normalize_organization_tags(self, organization_tags: List[str]) -> List[str]:
        normalized_organization_tags: List[str] = []

        for organization_tag in organization_tags:
            tag_doc = self.nlp_model(text=organization_tag)
    
            if len(tag_doc) > 0:
                tag_str = '-'.join(token.lemma_ for token in tag_doc) 
                normalized_organization_tags.append(self._normalize_token(tag_str))

        return normalized_organization_tags
                
    def _normalize_token(self, token: Union[Token, str]) -> str:
        if isinstance(token, str):
            return token.strip().lower()

        token_text_lemmatized = token.lemma_
        return token_text_lemmatized.strip().lower()

    def _is_token_important(self, token: Token) -> bool:
        if token.is_stop:
            return False

        if token.pos_ not in IMPORTANT_PARTS_OF_SPEECH:
            return False
        
        return True

    def extract_important_tokens(self) -> ExtractedTokenMap:
        if self.extracted_token_map is not None:
            return self.extracted_token_map

        extracted_token_map: ExtractedTokenMap = {}

        for token_batch in self.parser.get_token_batches():
            nlp_doc = self.nlp_model(text=token_batch.text)
            batch_page_number = token_batch.page_number 

            for token in nlp_doc:
                if self._is_token_important(token):
                    if batch_page_number not in extracted_token_map:
                        extracted_token_map[batch_page_number] = set()
                    
                    extracted_token_map[token_batch.page_number].add(self._normalize_token(token))

        self.extracted_token_map = extracted_token_map

        return extracted_token_map

    def fetch_extra_autotag_suggestions(self, word_tokens: List[Token], total_suggestions: int = 10) -> Set[str]:
        suggested_word_tokens: Set[str] = set()
        seen_word_tokens: Set[str] = set()

        while len(suggested_word_tokens) < total_suggestions:
            random_word_token = random.choice(word_tokens)
            if random_word_token.text not in seen_word_tokens:
                suggested_word_tokens.add(random_word_token.text)

            seen_word_tokens.add(random_word_token.text)

        return suggested_word_tokens


    def fetch_autotags(self) -> Tuple[Set[str], Set[str]]:
        if self.extracted_token_map is None:
            self.extract_important_tokens() 

        all_important_word_tokens: Set[Token] = set()

        for word_set in self.extracted_token_map.values():
            for word in word_set:
                word_token = self.nlp_model(text=word)[0]
                all_important_word_tokens.add(word_token)

        organization_tokens = [self.nlp_model(text=organization_tag) for organization_tag in self.organization_tags]  

        organization_autotags: Set[str] = set()

        for word_token in all_important_word_tokens:
            best_organization_token_matches_for_word_token: List[str] = []

            for organization_token in organization_tokens:
                similarity_score = word_token.similarity(organization_token)
                if similarity_score >= self.similarity_threshold:
                    best_organization_token_matches_for_word_token.append(self.organization_tag_mapping[organization_token.text])

            for word in best_organization_token_matches_for_word_token:
                organization_autotags.add(word)

        other_tag_suggestions = self.fetch_extra_autotag_suggestions(list(all_important_word_tokens), total_suggestions=20)

        return organization_autotags, other_tag_suggestions
        
        
        

