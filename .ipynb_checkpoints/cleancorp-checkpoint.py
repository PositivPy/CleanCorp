import re, string, collections, functools, unicodedata

from termdata import terms_by_country, terms_by_type, terms_by_industry

def build_term_set(input_dic):
    """ 
    Build tuples and sort by term length 
    @input: {'key' : [term_list], } 
    @return: [[key, term ], ]
    """
    tuple_list = []
    for key in input_dic:
        for item in input_dic[key]:
            temp_tuple = key, item
            tuple_list.append(temp_tuple)
            
    tuple_list = sorted(tuple_list, key=lambda part: len(part[1]), reverse=True)
    
    return tuple_list

# business_types / abbreviation 
SORTED_TYPES = build_term_set(terms_by_type)
# country / abbreviations 
SORTED_COUNTRIES = build_term_set(terms_by_country)
# industry / term 
SORTED_INDUSTRIES = build_term_set(terms_by_industry)

# All abbreviations sorted by length
all_sorted = SORTED_TYPES + SORTED_COUNTRIES
all_suffix = [item for key, item in all_sorted]
SORTED_SUFFIX = sorted(all_suffix, key=lambda x: len(x), reverse=True)

ALL_TERMS = SORTED_SUFFIX + [term for key, term in SORTED_INDUSTRIES]

class CleanCorp:
    def __init__(self, business_name):
        self.original_name = business_name

    @property
    @functools.lru_cache()
    def _sanitized_name(self): 
        """ Sanitize the orignal string """
        original_name = self.original_name 
        
        # Replacing comma with space
        sanitized = original_name.replace(',', ' ').replace(u"\uFF0C", ' ')
        
        # Get rid of extra spaces
        sanitized = " ".join(sanitized.split()).lower()
        
        # Get rid of all trailing punctuation except '.'
        match = re.search(r'[^\.\w]+$', sanitized, flags=re.UNICODE)
        if match:
            sanitized = sanitized[:match.span()[0]]

        return sanitized

    def _match_terms(self, term_set):
        """ 
        Match terms found in business_name to corresponding keys
        @input: [[key, term], ]
        @return: [key, ]
        """
        business_name = self._sanitized_name
        
        found_terms = []
        for key, term in term_set:
            # Composite terms (pty ltd, s de rl, ...)
            if ' ' in term and business_name.find(term) > 0:
                found_terms.append(key)
            # Simple terms (ltd., a.g., ...)
            elif term in business_name.split():
                found_terms.append(key) 

        # this sucks 
        found_terms = sorted(set(found_terms), reverse=True)

        if found_terms: return found_terms 
        else: return None 
        
    def _remove_terms(self, term_list):
        """ Returns business_name without terms in term_list """
        business_name = self._sanitized_name
        
        for term in term_list:
            # Composite terms ("pty ltd", "s de rl", ...)
            if ' ' in term and business_name.find(term) > 0:
                business_name = business_name.replace(term, '')
            # Single word terms
            elif term in business_name.split():
                business_name = business_name.replace(term, '')
                
        return " ".join(business_name.split())

    @property
    @functools.lru_cache()
    def clean_name(self):
        """ Clean company terms (ltd, corp, ...) from the business_name """
        _clean = self._remove_terms(SORTED_SUFFIX)
        return _clean
        

    @property
    @functools.lru_cache()
    def entity_type(self):
        """ Probable type of business entity """
        _type = self._match_terms(SORTED_TYPES)
        
        # if the entity type is not resolved but an industry term is found
        # the entity type is 'Unknown'
        if not _type and self.industry:
            _type = 'Unknown'
            
        return _type
    
    @property
    @functools.lru_cache()
    def country(self):
        """ Probable country of incorporation """
        return self._match_terms(SORTED_COUNTRIES)
    
    @property
    @functools.lru_cache()
    def industry(self):
        """ Probable industry """
        industry = self._match_terms(SORTED_INDUSTRIES)
        
        # If other industry terms are found, remove 'Unknown'
        if industry and len(industry) > 1 and 'Unknown' in industry:
            industry.remove('Unknown')
            
        return industry
        
    def is_company(self):
        """ True if any terms are found in the original name """
        if self.entity_type: return True
        else: return False
    
    def as_dict(self):
        """ Returns a dictionary of all the attributes """
        _dict = {'is_company' : self.is_company(),
                'original_name' : self.original_name, 
                'clean_name' : self.clean_name,
                'entity_type' : self.entity_type, 
                'industry' : self.industry, 
                'country' : self.country}
        return _dict
        
    def __repr__(self):
        """ Format the object's print: CleanCorp([original_name]) """
        _str = self.original_name
        return f'CleanCorp([{_str}])'
    
    