# CleanCorp - clean business names

Corpus based business entity reconciliation.

## Description

This Python package processes company names, provides a clean version of the
business name by stripping away terms indicating organization type (such as "Ltd." or "Corp") and attempts to extract the root name of the company by removing industry markers (such as "Metals", "Solar", "Banking", etc ...).

Using an organization type to suffix database, it also provides an utility to deduce the
type of organization, in terms of US/UK business entity types (ie. "limited liability
company" or "non-profit").

Furthermore, thanks to a multilingual annotated corpus, terms such as "Analytics" or "Accounting" are matched to their respective industries ('Technology', 'Financial Services'). 

Finally, the system uses the suffix' information to suggest countries the organization could
be established in. For example, the term "Oy" in a company's name it suggests it is established
in Finland, whereas "Ltd" in company name could mean UK, US or a number of other
countries.

## Disclamer

This package is not a replacement for a name reconcialiation service such as OpenCorporate's but rather a helper library to gain insights on un-reconciliable data. 

Milage may vary depending on typos and formating. You still have to clean your data... sorry. 

## Install

`pip3 install git+https://github.com/Syker.uk/cleancorp.git`

## Code

    >>> from cleancorp import CleanCorp

Initialize the instance with your business string:

    >>> business_name = "Some Big Pharma, LLC"
    >>> x = CleanCorp(business_name)
    >>> print(x)
    CleanCorp([Some Big Pharma, LLC])
    
You can now access CleanCorp's properties and attributes:

     >>> x.is_company()
    True

    >>> x.entity_type
    ['Limited Liability Company']
    
    >>> x.industry
    ['Health Care']

    >>> x.country
    ['United States of America', 'Philippines']

    >>> x.clean_name
    'Some Big Pharma'
    
    >>> x.root_name
    'Some Big'
    
     >>> x.as_dict()
    {
        'is_company' : True,
        'original_name' : 'Some Big Pharma, LLC', 
        'clean_name' : 'Some Big Pharma', 
        'root_name' : 'Some Big', 
        'entity_type' : ['Limited Liability Company'], 
        'industry' : ['Health Care'], 
        'country' : ['United States of America', 'Philippines']
    }
    
## Test

Run the test.ipynb notebook.

## The Data:

Suffix to Country to Entity Type data was compiled with OpenRefine from multiple sources, notably: 
- Wikipedia: [Types of Business Entity article](http://en.wikipedia.org/wiki/Types_of_business_entity)
- GLEIF (Global Legal Entity Identifier Foundation): [ISO 20275: Entity Legal Forms (ELF) Code List](https://www.gleif.org/en/about-lei/code-lists/iso-20275-entity-legal-forms-code-list)
- CorporateInformation: [Company Extensions and Security Identifiers](https://www.corporateinformation.com/Company-Extensions-Security-Identifiers.aspx)
The data is now maintained on wikipedia: [List of Business Entities by Country](http://en.wikipedia.org/wiki/)

Test data was provided by: 
- CDN and The Sunday Times [Panama Papers Dataset](https://cdn.rawgit.com/times/data/master/sunday_times_panama_data.zip)
- https://www.sec.gov/divisions/corpfin/internatl/alpha2002.html

The corpus of industry terms was compiled from kaggle's [7+ Million Company Dataset](https://www.kaggle.com/peopledatalabssf/free-7-million-company-dataset). 

## Credits
- Paul Solin: <paul@paulsolin.com> and contributor Petri Savolainen: <petri.savolainen@koodaamo.fi> for [cleanco](github) wich was more than just an inspiration for this package.
- CDN and The Sunday Time [Dataset](https://cdn.rawgit.com/times/data/master/sunday_times_panama_data.zip)
- Wikipedia: [Types of Business Entity article](http://en.wikipedia.org/wiki/Types_of_business_entity)
- GLEIF (Global Legal Entity Identifier Foundation): [ISO 20275: Entity Legal Forms (ELF) Code List](https://www.gleif.org/en/about-lei/code-lists/iso-20275-entity-legal-forms-code-list)
- CorporateInformation: [Company Extensions and Security Identifiers](https://www.corporateinformation.com/Company-Extensions-Security-Identifiers.aspx)
- Kaggle: [7+ Million Company Dataset](https://www.kaggle.com/peopledatalabssf/free-7-million-company-dataset)
