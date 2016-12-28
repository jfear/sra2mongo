"""Tests for mongo_schema.py"""
from textwrap import dedent
from sramongo.mongo_schema import URLLink, Xref, XrefLink, \
        EntrezLink, DDBJLink, ENALink, Submission, Organization, \
        Study


def test_URLLink_str_complete():
    url = URLLink(label='test', url='http://test.com')
    assert str(url) == 'label: test\nurl: http://test.com\n'


def test_URLLink_str_nolabel():
    url = URLLink(url='http://test.com')
    assert str(url) == 'label: None\nurl: http://test.com\n'


def test_URLLink_str_nourl():
    url = URLLink(label='test')
    assert str(url) == 'label: test\nurl: None\n'


def test_Xref_str_complete():
    xref = Xref(db='test', id='1030')
    assert str(xref) == 'db: test\nid: 1030\n'


def test_XrefLink_str_complete():
    xref = XrefLink(db='test', id='1030', label='test label')
    assert str(xref) == 'label: test label\ndb: test\nid: 1030\n'


def test_EntrezLink_str_complete():
    xref = EntrezLink(db='test', id='1030', label='test label',
                      query='Test[orgn]')
    assert str(xref) == ('label: test label\n'
                         'db: test\n'
                         'id: 1030\n'
                         'query: Test[orgn]\n')


def test_DDBJLink_str_complete():
    xref = DDBJLink(db='test', id='1030', label='test label',
                    url='http://test.com')
    assert str(xref) == ('label: test label\n'
                         'db: test\n'
                         'id: 1030\n'
                         'url: http://test.com\n')


def test_ENALink_str_complete():
    xref = ENALink(db='test', id='1030', label='test label',
                   url='http://test.com')
    assert str(xref) == ('label: test label\n'
                         'db: test\n'
                         'id: 1030\n'
                         'url: http://test.com\n')


def test_Submission_str_complete():
    submission = Submission(submission_id='SRA12345', broker='GEO')
    submission.external_id.append(Xref(**{'db': 'test', 'id': '1030'}))
    submission.external_id.append(Xref(**{'db': 'test2', 'id': '1032'}))
    submission.external_id.append(Xref(**{'db': 'test3', 'id': '1033'}))
    submission.submitter_id.append(
            Xref(**{'db': 'test', 'id': 'test submitter'}))

    assert str(submission).strip() == dedent("""\
        submission_id: SRA12345
        broker: GEO
        external_id:
            db: test, id: 1030
            db: test2, id: 1032
            db: test3, id: 1033
        secondary_id: None
        submitter_id:
            db: test, id: test submitter""")


def test_Organization_str_complete():
    organization = Organization(
        type='center', abbreviation='GEO', name='NCBI',
        email='geo@nih.gov', first_name='GEO', last_name='Curators')

    assert str(organization) == dedent("""\
        type: center
        abbreviation: GEO
        name: NCBI
        email: geo@nih.gov
        first_name: GEO
        last_name: Curators
        """)

STUDY = """\
study_id: SRA12345
GEO: GSE12345
GEO_Dataset: None
BioProject: PRJN1234
pubmed: 123456
external_id:
    db: test, id: 1030
    db: test2, id: 1032
    db: test3, id: 1033
secondary_id: None
submitter_id:
    db: test, id: test submitter
title: Test title
type: Test type
abstract: A very long abstract with more than 80 characters per line. A very long
          abstract with more than 80 characters per line. A very long abstract with
          more than 80 characters per line. A very long abstract with more than 80
          characters per line.
center_name: None
center_project_name: Test center
description: None
related_studies: None
url_links:
    label: test, url: http://test.com
xref_links: None
entrez_links: None
ddbj_links: None
ena_links: None
submission: None
organization:
    type: center
    abbreviation: GEO
    name: NCBI
    email: geo@nih.gov
    first_name: GEO
    last_name: Curators"""


def test_Study_str_partial():
    abstract = ('A very long abstract with more than 80 characters per line. '
                'A very long abstract with more than 80 characters per line. '
                'A very long abstract with more than 80 characters per line. '
                'A very long abstract with more than 80 characters per line.')

    study = Study(
        study_id='SRA12345', GEO='GSE12345', BioProject='PRJN1234',
        pubmed='123456', title='Test title', type='Test type',
        abstract=abstract, center_project_name='Test center')

    study.external_id.append(Xref(**{'db': 'test', 'id': '1030'}))
    study.external_id.append(Xref(**{'db': 'test2', 'id': '1032'}))
    study.external_id.append(Xref(**{'db': 'test3', 'id': '1033'}))
    study.submitter_id.append(Xref(**{'db': 'test', 'id': 'test submitter'}))

    study.url_links.append(
            URLLink(**{'label': 'test', 'url': 'http://test.com'}))

    study.organization = Organization(
        type='center', abbreviation='GEO', name='NCBI',
        email='geo@nih.gov', first_name='GEO', last_name='Curators')

    assert str(study) == STUDY

