from .models import Pubmed
from .xml_helpers import get_xml_text, get_xml_attribute


def parse_pubmed(root):
    pubmed = Pubmed()
    pubmed.accn = get_xml_text(root, 'PubmedArticle/MedlineCitation/PMID')
    pubmed.authors = get_authors(root)
    pubmed.title = get_xml_text(root, 'PubmedArticle/MedlineCitation/Article/ArticleTitle')
    pubmed.abstract = get_abstract(root)
    pubmed.journal = get_xml_text(root, 'PubmedArticle/MedlineCitation/Article/Journal/ISOAbbreviation')

    pubmed.volume = int(
        get_xml_text(root, 'PubmedArticle/MedlineCitation/Article/Journal/JournalIssue/Volume')
    )
    pubmed.page = int(
        get_xml_text(root, 'PubmedArticle/MedlineCitation/Article/Pagination/MedlinePgn')
    )
    pubmed.year = int(
        get_xml_text(root, 'PubmedArticle/MedlineCitation/Article/Journal/JournalIssue/PubDate/Year')
    )

    pubmed.date_created = get_date(root, 'PubmedArticle/MedlineCitation/DateCreated')
    pubmed.date_completed = get_date(root, 'PubmedArticle/MedlineCitation/DateCompleted')
    pubmed.date_revised = get_date(root, 'PubmedArticle/MedlineCitation/DateRevised')

    pubmed.citation = create_citation(pubmed)
    return pubmed


def get_abstract(root):
    text = [
        paragraph.text
        for paragraph in root.findall('PubmedArticle/MedlineCitation/Article/Abstract/AbstractText')
    ]
    return '\n'.join(text)


def get_authors(root):
    authors = []
    for author in root.findall('PubmedArticle/MedlineCitation/Article/AuthorList/Author'):
        authors.append(
            {
                'first_name': get_xml_text(author, 'ForeName'),
                'last_name': get_xml_text(author, 'LastName'),
                'initials': get_xml_text(author, 'Initials'),
                'affiliation': get_xml_text(author, 'AffiliationInfo/Affiliation'),
            }
        )
    return authors


def get_date(root, path):
    # TODO: Add correct datetime formats.
    curr_path = root.find(path)
    year = curr_path.find('Year').text
    month = curr_path.find('Month').text
    day = curr_path.find('Day').text
    return f'{year}-{month}-{day}'


def create_citation(pubmed):

    return (f'{pubmed.authors[0]["last_name"]}, {pubmed.authors[0]["first_name"]}, '
            f'et al. {pubmed.journal} {pubmed.volume} ({pubmed.year}): {pubmed.page}.')
