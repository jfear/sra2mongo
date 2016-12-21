#!/usr/bin/env python
""" Set up MonoDB schema using monogodngine. """
from mongoengine import Document, StringField, ListField, \
        EmbeddedDocumentField, EmbeddedDocument, ReferenceField, DictField

LIBRARY_STRATEGY = [
    "WGS",
    "WGA",
    "WXS",
    "RNA-Seq",
    "miRNA-Seq",
    "WCS",
    "CLONE",
    "POOLCLONE",
    "AMPLICON",
    "CLONEEND",
    "FINISHING",
    "ChIP-Seq",
    "MNase-Seq",
    "DNase-Hypersensitivity",
    "Bisulfite-Seq",
    "EST",
    "FL-cDNA",
    "CTS",
    "MRE-Seq",
    "MeDIP-Seq",
    "MBD-Seq",
    "Tn-Seq",
    "OTHER",
    ]

LIBRARY_SOURCE = [
    "GENOMIC",
    "TRANSCRIPTOMIC",
    "METAGENOMIC",
    "METATRANSCRIPTOMIC",
    "NON GENOMIC",
    "SYNTHETIC",
    "VIRAL RNA",
    "OTHER",
    ]

LIBRARY_SELECTION = [
    "RANDOM",
    "PCR",
    "RANDOM PCR",
    "RT-PCR",
    "HMPR",
    "MF",
    "CF-S",
    "CF-M",
    "CF-H",
    "CF-T",
    "MSLL",
    "cDNA",
    "ChIP",
    "MNase",
    "DNAse",
    "Hybrid Selection",
    "Reduced Representation",
    "Restriction Digest",
    "5-methylcytidine antibody",
    "MBD2 protein methyl-CpG binding domain",
    "CAGE",
    "RACE",
    "size fractionation",
    "MDA",
    "padlock probes capture method",
    "other",
    "unspecified",
    ]

PLATFORMS = [
    "LS454",
    "ILLUMINA",
    "HELICOS",
    "ABI_SOLID",
    "COMPLETE_GENOMICS",
    "PACBIO_SMRT",
    "ION_TORRENT",
    "CAPILLARY",
    ]



class URLLink(EmbeddedDocument):
    label = StringField()
    url = StringField()


class Xref(EmbeddedDocument):
    db = StringField()
    id = StringField()


class XrefLink(EmbeddedDocument):
    label = StringField()
    db = StringField()
    id = StringField()
    meta = {'allow_inheritance': True}


class EntrezLink(XrefLink):
    query = StringField()


class DDBJLink(XrefLink):
    url = StringField()


class ENALink(XrefLink):
    url = StringField()


class Organization(EmbeddedDocument):
    #SRA/EXPERIMENT/Organization@type
    type = StringField()

    #SRA/EXPERIMENT/Organization/Name@abbr
    abbreviation = StringField()

    #SRA/EXPERIMENT/Organization/Name.text
    name = StringField()

    #SRA/EXPERIMENT/Organization/Contact@email
    email = StringField()

    #SRA/EXPERIMENT/Organization/Contact/Name/First.text
    first_name = StringField()

    #SRA/EXPERIMENT/Organization/Contact/Name/Last.text
    last_name = StringField()


class Pool(EmbeddedDocument):
    samples = ListField(DictField)


class Submission(EmbeddedDocument):
    #SRA/EXPERIMENT/SUBMISSION/IDENTIFIERS/PRIMARY_ID.text
    submission_id = StringField(required=True, unique=True)

    #SRA/EXPERIMENT/SUBMISSION/IDENTIFIERS/EXTERNAL_ID@namespace
    #SRA/EXPERIMENT/SUBMISSION/IDENTIFIERS/EXTERNAL_ID.text
    external_id = ListField(EmbeddedDocumentField(Xref), default=list)

    #SRA/EXPERIMENT/SUBMISSION/IDENTIFIERS/SECONDARY_ID@namespace
    #SRA/EXPERIMENT/SUBMISSION/IDENTIFIERS/SECONDARY_ID.text
    secondary_id = ListField(EmbeddedDocumentField(Xref), default=list)

    #SRA/EXPERIMENT/SUBMISSION/IDENTIFIERS/SUBMITTER_ID@namespace
    #SRA/EXPERIMENT/SSUBMISSIONIDENTIFIERS/SUBMITTER_ID.text
    submitter_id = ListField(EmbeddedDocumentField(Xref), default=list)


class Study(Document):
    #SRA/EXPERIMENT/STUDY/IDENTIFIERS/PRIMARY_ID.text
    study_id = StringField(required=True, unique=True)

    submission = EmbeddedDocumentField(Submission)

    #SRA/EXPERIMENT/STUDY/IDENTIFIERS/EXTERNAL_ID@namespace
    #SRA/EXPERIMENT/STUDY/IDENTIFIERS/EXTERNAL_ID.text
    external_id = ListField(EmbeddedDocumentField(Xref), default=list)

    #SRA/EXPERIMENT/STUDY/IDENTIFIERS/SECONDARY_ID@namespace
    #SRA/EXPERIMENT/STUDY/IDENTIFIERS/SECONDARY_ID.text
    secondary_id = ListField(EmbeddedDocumentField(Xref), default=list)

    #SRA/EXPERIMENT/STUDY/IDENTIFIERS/SUBMITTER_ID@namespace
    #SRA/EXPERIMENT/STUDY/IDENTIFIERS/SUBMITTER_ID.text
    submitter_id = ListField(EmbeddedDocumentField(Xref), default=list)

    #SRA/EXPERIMENT/STUDY/DESCRIPTOR/STUDY_TITLE.text
    study_title = StringField()

    #SRA/EXPERIMENT/STUDY/DESCRIPTOR/STUDY_TYPE@existing_study_type or
    #SRA/EXPERIMENT/STUDY/DESCRIPTOR/STUDY_TYPE@new_study_type or
    #NOTE: VALIDATION @existing_study_type in EXISTING_STUDY_TYPES_*
    study_type = StringField()

    #SRA/EXPERIMENT/STUDY/DESCRIPTOR/STUDY_ABSTRACT
    study_abstract = StringField()

    #SRA/EXPERIMENT/STUDY@center_name or
    #NOTE: DEPRICATED SRA/EXPERIMENT/STUDY/DESCRIPTORM/CENTER_NAME.text
    center_name = StringField()

    #SRA/EXPERIMENT/STUDY/DESCRIPTOR/CENTER_PROJECT_NAME.text
    center_project_name = StringField()

    #SRA/EXPERIMENT/STUDY/DESCRIPTOR/STUDY_DESCRIPTION.text
    study_descriptor = StringField()

    # See Organization class for field defs
    organization = EmbeddedDocumentField(Organization)

    #[{'db': SRA/EXPERIMENT/STUDY/DESCRIPTOR/RELATED_STUDIES/RELATED_STUDY/RELATED_LINK/DB.text,
    #  'id': SRA/EXPERIMENT/STUDY/DESCRIPTOR/RELATED_STUDIES/RELATED_STUDY/RELATED_LINK/ID.text,
    #  'label': SRA/EXPERIMENT/STUDY/DESCRIPTOR/RELATED_STUDIES/RELATED_STUDY/RELATED_LINK/LABEL.text},
    #]
    related_studies = ListField(EmbeddedDocumentField(XrefLink), default=list)

    #SRA/EXPERIMENT/STUDY/DESCRIPTOR/RELATED_STUDIES/RELATED_STUDY/IS_PRIMARY.text
    primary_study = StringField()

    #{label: SRA/EXPERIMENT/STUDY/STUDY_LINKS/STUDY_LINK/URL_LINK/LABEL.text,
    # url: SRA/EXPERIMENT/STUDY/STUDY_LINKS/STUDY_LINK/URL_LINK/URL.text}
    url_link = ListField(EmbeddedDocumentField(URLLink), default=list)

    #{label: SRA/EXPERIMENT/STUDY/STUDY_LINKS/STUDY_LINK/XREF_LINK/LABEL.text,
    # db: SRA/EXPERIMENT/STUDY/STUDY_LINKS/STUDY_LINK/XREF_LINK/DB.text,
    # id: SRA/EXPERIMENT/STUDY/STUDY_LINKS/STUDY_LINK/XREF_LINK/ID.text}
    xref_link = ListField(EmbeddedDocumentField(XrefLink), default=list)

    #{label: SRA/EXPERIMENT/STUDY/STUDY_LINKS/STUDY_LINK/ENTREZ_LINK/LABEL.text,
    # db: SRA/EXPERIMENT/STUDY/STUDY_LINKS/STUDY_LINK/ENTREZ_LINK/DB.text,
    # id: SRA/EXPERIMENT/STUDY/STUDY_LINKS/STUDY_LINK/ENTREZ_LINK/ID.text,
    # query: SRA/EXPERIMENT/STUDY/STUDY_LINKS/STUDY_LINK/ENTREZ_LINK/QUERY.text}
    study_entrez_link = ListField(EmbeddedDocumentField(EntrezLink), default=list)

    #{label: SRA/EXPERIMENT/STUDY/STUDY_LINKS/STUDY_LINK/DDBJ_LINK/LABEL.text,
    # db: SRA/EXPERIMENT/STUDY/STUDY_LINKS/STUDY_LINK/DDBJ_LINK/DB.text,
    # id: SRA/EXPERIMENT/STUDY/STUDY_LINKS/STUDY_LINK/DDBJ_LINK/ID.text,
    # url: SRA/EXPERIMENT/STUDY/STUDY_LINKS/STUDY_LINK/DDBJ_LINK/URL.text}
    ddbj_link = ListField(EmbeddedDocumentField(DDBJLink), default=list)

    #{LABEL: SRA/EXPERIMENT/STUDY/STUDY_LINKS/STUDY_LINK/ENA_LINK/LABEL.text,
    # DB: SRA/EXPERIMENT/STUDY/STUDY_LINKS/STUDY_LINK/ENA_LINK/DB.text,
    # ID: SRA/EXPERIMENT/STUDY/STUDY_LINKS/STUDY_LINK/ENA_LINK/ID.text,
    # URL: SRA/EXPERIMENT/STUDY/STUDY_LINKS/STUDY_LINK/ENA_LINK/URL.text}
    ena_link = ListField(EmbeddedDocumentField(ENALink), default=list)


class Experiment(Document):
    #SRA/EXPERIMENT/IDENTIFIERS/PRIMARY_ID.text
    experiment_id = StringField(required=True, unique=True)

    # See study class for xpath
    study_id = ReferenceField(Study)

    #SRA/EXPERIMENT/IDENTIFIERS/EXTERNAL_ID.@namespace
    #SRA/EXPERIMENT/IDENTIFIERS/EXTERNAL_ID.text
    external_id = ListField(EmbeddedDocumentField(Xref), default=list)

    #SRA/EXPERIMENT/IDENTIFIERS/SECONDARY_ID@namespace
    #SRA/EXPERIMENT/IDENTIFIERS/SECONDARY_ID.text
    secondary_id = ListField(EmbeddedDocumentField(Xref), default=list)

    #SRA/EXPERIMENT/IDENTIFIERS/SUBMITTER_ID.@namespace
    #SRA/EXPERIMENT/IDENTIFIERS/SUBMITTER_ID.text
    submitter_id = ListField(EmbeddedDocumentField(Xref), default=list)

    #SRA/EXPERIMENT/TITLE.text
    title = StringField()

    #SRA/EXPERIMENT/STUDY_REF/IDENTIFIERS/PRIMARY_ID.text
    study = ReferenceField(Study)

    #SRA/EXPERIMENT/DESIGN/DESIGN_DESCRIPTION.text
    design_description = StringField()

    #SRA/EXPERIMENT/DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_NAME.text
    library_name = StringField()

    #SRA/EXPERIMENT/DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_STRATEGY.text
    #NOTE: VALIDATE: LIBRARY_STRATEGY
    library_strategy = StringField(choices=LIBRARY_STRATEGY)

    #SRA/EXPERIMENT/DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_SOURCE.text
    #NOTE: VALIDATE: LIBRARY_SOURCE
    library_source = StringField(choices=LIBRARY_SOURCE)

    #SRA/EXPERIMENT/DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_SELECTION.text
    #NOTE: VALIDATE: LIBRARY_SELECTION
    library_selection = StringField(choices=LIBRARY_SELECTION)

    #SRA/EXPERIMENT/DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_LAYOUT/SINGLE or
    #SRA/EXPERIMENT/DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_LAYOUT/PAIRED
    library_layout = StringField(choices=['SINGLE', 'PAIRED'])

    #SRA/EXPERIMENT/DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_LAYOUT/PAIRED@ORIENTATION
    library_layout_orientation = StringField()

    #SRA/EXPERIMENT/DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_LAYOUT/PAIRED@NOMINAL_LENGTH
    library_layout_nominal_length = StringField()

    #SRA/EXPERIMENT/DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_LAYOUT/PAIRED@NOMINAL_SDEV
    library_layout_nominal_sdev = StringField()

    #SRA/EXPERIMENT/DESIGN/LIBRARY_DESCRIPTOR/POOLING_STRATEGY.text
    pooling_strategey = StringField()

    #SRA/EXPERIMENT/DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_CONSTRUCTION_PROTOCOL.text
    library_contruction_protocol = StringField('library_construction_protocol')

    #SRA/EXPERIMENT/PLATFORM/<CLASS>
    platform = StringField(choices=PLATFORMS)

    #SRA/EXPERIMENT/PLATFORM/<CLASS>/INSTRUMENT_MODEL.text
    #NOTE: VALIDATE: PLATFORM_TYPE_ACTIVE, PLATFORM_TYPE_DEPRICATED
    instrument_model = StringField()

    #{label: SRA/EXPERIMENT/EXPERIMENT_LINKS/EXPERIMENT_LINK/URL_LINK/LABEL.text,
    # url: SRA/EXPERIMENT/EXPERIMENT_LINKS/EXPERIMENT_LINK/URL_LINK/URL.text}
    url_link = ListField(EmbeddedDocumentField(URLLink), default=list)

    #{label: SRA/EXPERIMENT/EXPERIMENT_LINKS/EXPERIMENT_LINK/XREF_LINK/LABEL.text,
    # db: SRA/EXPERIMENT/EXPERIMENT_LINKS/EXPERIMENT_LINK/XREF_LINK/DB.text,
    # id: SRA/EXPERIMENT/EXPERIMENT_LINKS/EXPERIMENT_LINK/XREF_LINK/ID.text}
    xref_link = ListField(EmbeddedDocumentField(XrefLink), default=list)

    #{label: SRA/EXPERIMENT/EXPERIMENT_LINKS/EXPERIMENT_LINK/ENTREZ_LINK/LABEL.text,
    # db: SRA/EXPERIMENT/EXPERIMENT_LINKS/EXPERIMENT_LINK/ENTREZ_LINK/DB.text,
    # id: SRA/EXPERIMENT/EXPERIMENT_LINKS/EXPERIMENT_LINK/ENTREZ_LINK/ID.text,
    # query: SRA/EXPERIMENT/EXPERIMENT_LINKS/EXPERIMENT_LINK/ENTREZ_LINK/QUERY.text}
    study_entrez_link = ListField(EmbeddedDocumentField(EntrezLink), default=list)

    #{label: SRA/EXPERIMENT/EXPERIMENT_LINKS/EXPERIMENT_LINK/DDBJ_LINK/LABEL.text,
    # db: SRA/EXPERIMENT/EXPERIMENT_LINKS/EXPERIMENT_LINK/DDBJ_LINK/DB.text,
    # id: SRA/EXPERIMENT/EXPERIMENT_LINKS/STUDY_LINK/DDBJ_LINK/ID.text,
    # url: SRA/EXPERIMENT/EXPERIMENT_LINKS/STUDY_LINK/DDBJ_LINK/URL.text}
    ddbj_link = ListField(EmbeddedDocumentField(DDBJLink), default=list)

    #{LABEL: SRA/EXPERIMENT/EXPERIMENT_LINKS/EXPERIMENT_LINK/ENA_LINK/LABEL.text,
    # DB: SRA/EXPERIMENT/EXPERIMENT_LINKS/EXPERIMENT_LINK/ENA_LINK/DB.text,
    # ID: SRA/EXPERIMENT/EXPERIMENT_LINKS/EXPERIMENT_LINK/ENA_LINK/ID.text,
    # URL: SRA/EXPERIMENT/EXPERIMENT_LINKS/EXPERIMENT_LINK/ENA_LINK/URL.text}
    ena_link = ListField(EmbeddedDocumentField(ENALink), default=list)

    #SRA/EXPERIMENT/EXPERIMENT_ATTRIBUTES/EXPERIMENT_ATTRIBUTE/TAG.text
    #SRA/EXPERIMENT/EXPERIMENT_ATTRIBUTES/EXPERIMENT_ATTRIBUTE/VALUE.text
    experiment_attribute = DictField()

    #SRA/Pool
    #NOTE: Only really care about primary_id (SRS), BioSample, Geo
    samples = EmbeddedDocument(Pool)


class Sample(Document):
    #SRA/EXPERIMENT/DESIGN/IDENTIFIERS/PRIMARY_ID.text
    sample_id = StringField(required=True, unique=True)

    #SRA/EXPERIMENT/IDENTIFIERS/EXTERNAL_ID.@namespace
    #SRA/EXPERIMENT/DESIGN/IDENTIFIERS/EXTERNAL_ID.text
    external_id = ListField(EmbeddedDocumentField(Xref), default=list)

    #SRA/EXPERIMENT/IDENTIFIERS/SECONDARY_ID@namespace
    #SRA/EXPERIMENT/DESIGN/IDENTIFIERS/SECONDARY_ID.text
    secondary_id = ListField(EmbeddedDocumentField(Xref), default=list)

    """
    <SAMPLE alias="GSM1471477" accession="SRS679015">
      <IDENTIFIERS>
        <PRIMARY_ID>SRS679015</PRIMARY_ID>
        <EXTERNAL_ID namespace="BioSample">SAMN02981965</EXTERNAL_ID>
        <EXTERNAL_ID namespace="GEO">GSM1471477</EXTERNAL_ID>
      </IDENTIFIERS>
      <TITLE>DGRP563 M_E3_2_L3</TITLE>
      <SAMPLE_NAME>
        <TAXON_ID>7227</TAXON_ID>
        <SCIENTIFIC_NAME>Drosophila melanogaster</SCIENTIFIC_NAME>
      </SAMPLE_NAME>
      <SAMPLE_LINKS>
        <SAMPLE_LINK>
          <XREF_LINK>
            <DB>bioproject</DB>
            <ID>258012</ID>
            <LABEL>PRJNA258012</LABEL>
          </XREF_LINK>
        </SAMPLE_LINK>
      </SAMPLE_LINKS>
      <SAMPLE_ATTRIBUTES>
        <SAMPLE_ATTRIBUTE>
          <TAG>source_name</TAG>
          <VALUE>Whole body</VALUE>
        </SAMPLE_ATTRIBUTE>
        <SAMPLE_ATTRIBUTE>
          <TAG>strain</TAG>
          <VALUE>DGRP-563</VALUE>
        </SAMPLE_ATTRIBUTE>
        <SAMPLE_ATTRIBUTE>
          <TAG>developmental stage</TAG>
          <VALUE>Adult</VALUE>
        </SAMPLE_ATTRIBUTE>
        <SAMPLE_ATTRIBUTE>
          <TAG>Sex</TAG>
          <VALUE>male</VALUE>
        </SAMPLE_ATTRIBUTE>
        <SAMPLE_ATTRIBUTE>
          <TAG>tissue</TAG>
          <VALUE>Whole body</VALUE>
        </SAMPLE_ATTRIBUTE>
      </SAMPLE_ATTRIBUTES>
    </SAMPLE>
    """


class Run(Document):
    #SRA/RUN_SET/RUN/IDENTIFIERS/PRIMARY_ID.text
    run_id = StringField(required=True, unique=True)

    #SRA/RUN_SET/RUN/EXPERIMENT_REF@accession
    experiment_id = ReferenceField(Experiment)

    #SRA/RUN_SET/RUN/IDENTIFIERS/EXTERNAL_ID.@namespace
    #SRA/EXPERIMENT/IDENTIFIERS/EXTERNAL_ID.text
    external_id = ListField(EmbeddedDocumentField(Xref), default=list)

    #SRA/RUN_SET/RUN/IDENTIFIERS/SECONDARY_ID@namespace
    #SRA/RUN_SET/RUN/IDENTIFIERS/SECONDARY_ID.text
    secondary_id = ListField(EmbeddedDocumentField(Xref), default=list)

    #SRA/RUN_SET/RUN/IDENTIFIERS/SUBMITTER_ID.@namespace
    #SRA/RUN_SET/RUN/IDENTIFIERS/SUBMITTER_ID.text
    submitter_id = ListField(EmbeddedDocumentField(Xref), default=list)

    #SRA/RUN_SET/RUN/Pool
    #NOTE: Only really care about primary_id (SRS), BioSample, Geo
    samples = EmbeddedDocument(Pool)

    """
    Column('run_date', Text),
    Column('run_file', Text),
    Column('run_center', Text),
    Column('total_data_blocks', Integer),
    Column('experiment_accession', Text),
    Column('experiment_name', Text),
    Column('sra_link', Text),
    Column('run_url_link', Text),
    Column('xref_link', Text),
    Column('run_entrez_link', Text),
    Column('ddbj_link', Text),
    Column('ena_link', Text),
    Column('run_attribute', Text),
    Column('submission_accession', Text),
    Column('sradb_updated', Text)

        <Pool>
          <Member member_name="" accession="SRS679015" sample_name="GSM1471477" sample_title="DGRP563 M_E3_2_L3" spots="2001211" bases="152092036" tax_id="7227" organism="Drosophila melanogaster">
            <IDENTIFIERS>
              <PRIMARY_ID>SRS679015</PRIMARY_ID>
              <EXTERNAL_ID namespace="BioSample">SAMN02981965</EXTERNAL_ID>
              <EXTERNAL_ID namespace="GEO">GSM1471477</EXTERNAL_ID>
            </IDENTIFIERS>
          </Member>
        </Pool>

        <Statistics nreads="1" nspots="2001211">
          <Read index="0" count="2001211" average="76" stdev="0"/>
        </Statistics>
        <Bases cs_native="false" count="152092036">
          <Base value="A" count="37700865"/>
          <Base value="C" count="34213516"/>
          <Base value="G" count="34694905"/>
          <Base value="T" count="44683416"/>
          <Base value="N" count="799334"/>
        </Bases>
    TAX
        <tax_analysis parser_version="0.4" dbs_mtime="2016-06-28 06:01:03" aligns_to_version="0.34" dbss_name="tree_filter.dbss" analyzed_spot_count="2001211" total_spot_count="2001211" dbss_mtime="2016-07-07 08:15:09" identified_spot_count="634270" dbs_name="tree_index.dbs">
          <taxon self_count="16" tax_id="131567" name="cellular organisms" total_count="634200">
            <taxon self_count="5904" tax_id="2759" rank="superkingdom" name="Eukaryota" total_count="530888">
              <taxon self_count="1068" tax_id="33154" name="Opisthokonta" total_count="524758">
                <taxon self_count="0" tax_id="33208" rank="kingdom" name="Metazoa" total_count="523525">
                  <taxon self_count="0" tax_id="6072" name="Eumetazoa" total_count="523525">
                    <taxon self_count="2605" tax_id="33213" name="Bilateria" total_count="523525">
                      <taxon self_count="125" tax_id="33317" name="Protostomia" total_count="360888">
                        <taxon self_count="0" tax_id="1206794" name="Ecdysozoa" total_count="360762">
                          <taxon self_count="0" tax_id="88770" name="Panarthropoda" total_count="360762">
                            <taxon self_count="154" tax_id="6656" rank="phylum" name="Arthropoda" total_count="360762">
                              <taxon self_count="0" tax_id="197563" name="Mandibulata" total_count="360608">
                                <taxon self_count="0" tax_id="197562" name="Pancrustacea" total_count="360608">
                                  <taxon self_count="0" tax_id="6960" rank="superclass" name="Hexapoda" total_count="360608">
                                    <taxon self_count="0" tax_id="50557" rank="class" name="Insecta" total_count="360608">
                                      <taxon self_count="0" tax_id="85512" name="Dicondylia" total_count="360608">
                                        <taxon self_count="0" tax_id="7496" name="Pterygota" total_count="360608">
                                          <taxon self_count="95" tax_id="33340" rank="subclass" name="Neoptera" total_count="360608">
                                            <taxon self_count="54977" tax_id="33392" rank="infraclass" name="Endopterygota" total_count="360513">
                                              <taxon self_count="724" tax_id="7147" rank="order" name="Diptera" total_count="305536">
                                                <taxon self_count="0" tax_id="7203" rank="suborder" name="Brachycera" total_count="304812">
                                                  <taxon self_count="0" tax_id="43733" rank="infraorder" name="Muscomorpha" total_count="304812">
                                                    <taxon self_count="0" tax_id="480118" name="Eremoneura" total_count="304812">
                                                      <taxon self_count="9" tax_id="480117" name="Cyclorrhapha" total_count="304812">
                                                        <taxon self_count="1728" tax_id="43738" name="Schizophora" total_count="304803">
                                                          <taxon self_count="1020" tax_id="43741" name="Acalyptratae" total_count="303071">
                                                            <taxon self_count="0" tax_id="43746" rank="superfamily" name="Ephydroidea" total_count="302045">
                                                            <taxon self_count="0" tax_id="7214" rank="family" name="Drosophilidae" total_count="302045">
                                                            <taxon self_count="0" tax_id="43845" rank="subfamily" name="Drosophilinae" total_count="302045">
                                                            <taxon self_count="0" tax_id="46877" rank="tribe" name="Drosophilini" total_count="302045">
                                                            <taxon self_count="4881" tax_id="7215" rank="genus" name="Drosophila" total_count="302045">
                                                            <taxon self_count="8326" tax_id="32341" rank="subgenus" name="Sophophora" total_count="296762">
                                                            <taxon self_count="6773" tax_id="32346" rank="species group" name="melanogaster group" total_count="287735">
                                                            <taxon self_count="0" tax_id="32347" rank="species subgroup" name="ananassae subgroup" total_count="221">
                                                            <taxon self_count="0" tax_id="545632" name="ananassae species complex" total_count="221">
                                                            <taxon self_count="221" tax_id="7217" rank="species" name="Drosophila ananassae" total_count="221"/>
                                                            </taxon>
                                                            </taxon>
                                                            <taxon self_count="227907" tax_id="32351" rank="species subgroup" name="melanogaster subgroup" total_count="280741">
                                                            <taxon self_count="7437" tax_id="7220" rank="species" name="Drosophila erecta" total_count="7437"/>
                                                            <taxon self_count="2179" tax_id="7227" rank="species" name="Drosophila melanogaster" total_count="2179"/>
                                                            <taxon self_count="15094" tax_id="7238" rank="species" name="Drosophila sechellia" total_count="15094"/>
                                                            <taxon self_count="22217" tax_id="7240" rank="species" name="Drosophila simulans" total_count="22217"/>
                                                            <taxon self_count="5907" tax_id="7245" rank="species" name="Drosophila yakuba" total_count="5907"/>
                                                            </taxon>
                                                            </taxon>
                                                            <taxon self_count="0" tax_id="32365" rank="species group" name="willistoni group" total_count="539">
                                                            <taxon self_count="0" tax_id="32367" rank="species subgroup" name="willistoni subgroup" total_count="539">
                                                            <taxon self_count="539" tax_id="7260" rank="species" name="Drosophila willistoni" total_count="539"/>
                                                            </taxon>
                                                            </taxon>
                                                            <taxon self_count="0" tax_id="32355" rank="species group" name="obscura group" total_count="162">
                                                            <taxon self_count="162" tax_id="32358" rank="species subgroup" name="pseudoobscura subgroup" total_count="162"/>
                                                            </taxon>
                                                            </taxon>
                                                            <taxon self_count="0" tax_id="32281" rank="subgenus" name="Drosophila" total_count="402">
                                                            <taxon self_count="0" tax_id="32335" rank="species group" name="virilis group" total_count="398">
                                                            <taxon self_count="398" tax_id="7244" rank="species" name="Drosophila virilis" total_count="398"/>
                                                            </taxon>
                                                            <taxon self_count="0" tax_id="306032" rank="species group" name="flavopilosa group" total_count="3">
                                                            <taxon self_count="0" tax_id="306034" rank="species subgroup" name="nesiota subgroup" total_count="3">
                                                            <taxon self_count="3" tax_id="306035" rank="species" name="Drosophila incompta" total_count="3"/>
                                                            </taxon>
                                                            </taxon>
                                                            <taxon self_count="0" tax_id="32304" rank="species group" name="immigrans group" total_count="1">
                                                            <taxon self_count="0" tax_id="32306" rank="species subgroup" name="immigrans subgroup" total_count="1">
                                                            <taxon self_count="1" tax_id="157056" rank="species" name="Drosophila formosana" total_count="1"/>
                                                            </taxon>
                                                            </taxon>
                                                            </taxon>
                                                            </taxon>
                                                            </taxon>
                                                            </taxon>
                                                            </taxon>
                                                            </taxon>
                                                            <taxon self_count="0" tax_id="43752" rank="superfamily" name="Tephritoidea" total_count="6">
                                                            <taxon self_count="0" tax_id="7211" rank="family" name="Tephritidae" total_count="6">
                                                            <taxon self_count="0" tax_id="164860" rank="subfamily" name="Dacinae" total_count="6">
                                                            <taxon self_count="0" tax_id="43871" rank="tribe" name="Dacini" total_count="6">
                                                            <taxon self_count="0" tax_id="27456" rank="genus" name="Bactrocera" total_count="6">
                                                            <taxon self_count="0" tax_id="69624" rank="subgenus" name="Daculus" total_count="5">
                                                            <taxon self_count="5" tax_id="104688" rank="species" name="Bactrocera oleae" total_count="5"/>
                                                            </taxon>
                                                            <taxon self_count="0" tax_id="47832" rank="subgenus" name="Bactrocera" total_count="1">
                                                            <taxon self_count="1" tax_id="98805" name="Bactrocera dorsalis species complex" total_count="1"/>
                                                            </taxon>
                                                            </taxon>
                                                            </taxon>
                                                            </taxon>
                                                            </taxon>
                                                            </taxon>
                                                          </taxon>
                                                          <taxon self_count="0" tax_id="43742" name="Calyptratae" total_count="4">
                                                            <taxon self_count="0" tax_id="43755" rank="superfamily" name="Oestroidea" total_count="4">
                                                            <taxon self_count="3" tax_id="7371" rank="family" name="Calliphoridae" total_count="4">
                                                            <taxon self_count="0" tax_id="43913" rank="subfamily" name="Chrysomyinae" total_count="1">
                                                            <taxon self_count="0" tax_id="54281" rank="tribe" name="Chrysomyini" total_count="1">
                                                            <taxon self_count="1" tax_id="45449" rank="genus" name="Chrysomya" total_count="1"/>
                                                            </taxon>
                                                            </taxon>
                                                            </taxon>
                                                            </taxon>
                                                          </taxon>
                                                        </taxon>
                                                      </taxon>
                                                    </taxon>
                                                  </taxon>
                                                </taxon>
                                              </taxon>
                                            </taxon>
                                          </taxon>
                                        </taxon>
                                      </taxon>
                                    </taxon>
                                  </taxon>
                                </taxon>
                              </taxon>
                            </taxon>
                          </taxon>
                        </taxon>
                        <taxon self_count="0" tax_id="1206795" name="Lophotrochozoa" total_count="1">
                          <taxon self_count="0" tax_id="6447" rank="phylum" name="Mollusca" total_count="1">
                            <taxon self_count="0" tax_id="6650" rank="class" name="Polyplacophora" total_count="1">
                              <taxon self_count="0" tax_id="6651" rank="order" name="Neoloricata" total_count="1">
                                <taxon self_count="0" tax_id="6652" rank="suborder" name="Chitonida" total_count="1">
                                  <taxon self_count="0" tax_id="291862" name="Chitonina" total_count="1">
                                    <taxon self_count="0" tax_id="39684" rank="family" name="Chitonidae" total_count="1">
                                      <taxon self_count="0" tax_id="291881" rank="subfamily" name="Chitoninae" total_count="1">
                                        <taxon self_count="1" tax_id="256426" rank="genus" name="Sypharochiton" total_count="1"/>
                                      </taxon>
                                    </taxon>
                                  </taxon>
                                </taxon>
                              </taxon>
                            </taxon>
                          </taxon>
                        </taxon>
                      </taxon>
                      <taxon self_count="0" tax_id="33511" name="Deuterostomia" total_count="160032">
                        <taxon self_count="0" tax_id="7711" rank="phylum" name="Chordata" total_count="160032">
                          <taxon self_count="0" tax_id="89593" rank="subphylum" name="Craniata" total_count="160032">
                            <taxon self_count="0" tax_id="7742" name="Vertebrata" total_count="160032">
                              <taxon self_count="0" tax_id="7776" name="Gnathostomata" total_count="160032">
                                <taxon self_count="0" tax_id="117570" name="Teleostomi" total_count="160032">
                                  <taxon self_count="233" tax_id="117571" name="Euteleostomi" total_count="160032">
                                    <taxon self_count="15" tax_id="8287" name="Sarcopterygii" total_count="159799">
                                      <taxon self_count="0" tax_id="1338369" name="Dipnotetrapodomorpha" total_count="159784">
                                        <taxon self_count="0" tax_id="32523" name="Tetrapoda" total_count="159784">
                                          <taxon self_count="689" tax_id="32524" name="Amniota" total_count="159784">
                                            <taxon self_count="27" tax_id="40674" rank="class" name="Mammalia" total_count="158518">
                                              <taxon self_count="84" tax_id="32525" name="Theria" total_count="158491">
                                                <taxon self_count="1248" tax_id="9347" name="Eutheria" total_count="158407">
                                                  <taxon self_count="2153" tax_id="1437010" name="Boreoeutheria" total_count="157159">
                                                    <taxon self_count="1727" tax_id="314146" rank="superorder" name="Euarchontoglires" total_count="154547">
                                                      <taxon self_count="2797" tax_id="9443" rank="order" name="Primates" total_count="149496">
                                                        <taxon self_count="1008" tax_id="376913" rank="suborder" name="Haplorrhini" total_count="146699">
                                                          <taxon self_count="17696" tax_id="314293" rank="infraorder" name="Simiiformes" total_count="145675">
                                                            <taxon self_count="25883" tax_id="9526" rank="parvorder" name="Catarrhini" total_count="127979">
                                                            <taxon self_count="19974" tax_id="314295" rank="superfamily" name="Hominoidea" total_count="102096">
                                                            <taxon self_count="15408" tax_id="9604" rank="family" name="Hominidae" total_count="82122">
                                                            <taxon self_count="42073" tax_id="207598" rank="subfamily" name="Homininae" total_count="66714">
                                                            <taxon self_count="51" tax_id="9605" rank="genus" name="Homo" total_count="24569">
                                                            <taxon self_count="24516" tax_id="9606" rank="species" name="Homo sapiens" total_count="24518">
                                                            <taxon self_count="2" tax_id="63221" rank="subspecies" name="Homo sapiens neanderthalensis" total_count="2"/>
                                                            </taxon>
                                                            </taxon>
                                                            <taxon self_count="0" tax_id="9592" rank="genus" name="Gorilla" total_count="72">
                                                            <taxon self_count="0" tax_id="9593" rank="species" name="Gorilla gorilla" total_count="72">
                                                            <taxon self_count="72" tax_id="9595" rank="subspecies" name="Gorilla gorilla gorilla" total_count="72"/>
                                                            </taxon>
                                                            </taxon>
                                                            </taxon>
                                                            </taxon>
                                                            </taxon>
                                                            </taxon>
                                                          </taxon>
                                                          <taxon self_count="0" tax_id="376912" rank="infraorder" name="Tarsiiformes" total_count="16">
                                                            <taxon self_count="0" tax_id="9475" rank="family" name="Tarsiidae" total_count="16">
                                                            <taxon self_count="0" tax_id="1868481" rank="genus" name="Carlito" total_count="16">
                                                            <taxon self_count="16" tax_id="9478" rank="species" name="Carlito syrichta" total_count="16"/>
                                                            </taxon>
                                                            </taxon>
                                                          </taxon>
                                                        </taxon>
                                                      </taxon>
                                                      <taxon self_count="0" tax_id="314147" name="Glires" total_count="3324">
                                                        <taxon self_count="0" tax_id="9989" rank="order" name="Rodentia" total_count="3324">
                                                          <taxon self_count="0" tax_id="33553" rank="suborder" name="Sciurognathi" total_count="3323">
                                                            <taxon self_count="101" tax_id="337687" name="Muroidea" total_count="3323">
                                                            <taxon self_count="0" tax_id="10066" rank="family" name="Muridae" total_count="3222">
                                                            <taxon self_count="0" tax_id="39107" rank="subfamily" name="Murinae" total_count="3222">
                                                            <taxon self_count="0" tax_id="10088" rank="genus" name="Mus" total_count="3222">
                                                            <taxon self_count="0" tax_id="862507" rank="subgenus" name="Mus" total_count="3222">
                                                            <taxon self_count="3222" tax_id="10090" rank="species" name="Mus musculus" total_count="3222"/>
                                                            </taxon>
                                                            </taxon>
                                                            </taxon>
                                                            </taxon>
                                                            </taxon>
                                                          </taxon>
                                                          <taxon self_count="0" tax_id="33550" rank="suborder" name="Hystricognathi" total_count="1">
                                                            <taxon self_count="0" tax_id="10139" rank="family" name="Caviidae" total_count="1">
                                                            <taxon self_count="0" tax_id="10140" rank="genus" name="Cavia" total_count="1">
                                                            <taxon self_count="1" tax_id="10141" rank="species" name="Cavia porcellus" total_count="1"/>
                                                            </taxon>
                                                            </taxon>
                                                          </taxon>
                                                        </taxon>
                                                      </taxon>
                                                    </taxon>
                                                    <taxon self_count="0" tax_id="314145" rank="superorder" name="Laurasiatheria" total_count="459">
                                                      <taxon self_count="0" tax_id="91561" name="Cetartiodactyla" total_count="397">
                                                        <taxon self_count="0" tax_id="35497" rank="infraorder" name="Suina" total_count="160">
                                                          <taxon self_count="0" tax_id="9821" rank="family" name="Suidae" total_count="160">
                                                            <taxon self_count="0" tax_id="9822" rank="genus" name="Sus" total_count="160">
                                                            <taxon self_count="160" tax_id="9823" rank="species" name="Sus scrofa" total_count="160"/>
                                                            </taxon>
                                                          </taxon>
                                                        </taxon>
                                                        <taxon self_count="0" tax_id="9845" rank="suborder" name="Ruminantia" total_count="237">
                                                          <taxon self_count="0" tax_id="35500" rank="infraorder" name="Pecora" total_count="237">
                                                            <taxon self_count="87" tax_id="9895" rank="family" name="Bovidae" total_count="237">
                                                            <taxon self_count="0" tax_id="9948" rank="subfamily" name="Antilopinae" total_count="8">
                                                            <taxon self_count="0" tax_id="59537" rank="genus" name="Pantholops" total_count="8">
                                                            <taxon self_count="8" tax_id="59538" rank="species" name="Pantholops hodgsonii" total_count="8"/>
                                                            </taxon>
                                                            </taxon>
                                                            <taxon self_count="142" tax_id="27592" rank="subfamily" name="Bovinae" total_count="142"/>
                                                            </taxon>
                                                          </taxon>
                                                        </taxon>
                                                      </taxon>
                                                      <taxon self_count="0" tax_id="33554" rank="order" name="Carnivora" total_count="62">
                                                        <taxon self_count="0" tax_id="379584" rank="suborder" name="Caniformia" total_count="62">
                                                          <taxon self_count="0" tax_id="9608" rank="family" name="Canidae" total_count="62">
                                                            <taxon self_count="0" tax_id="9611" rank="genus" name="Canis" total_count="62">
                                                            <taxon self_count="0" tax_id="9612" rank="species" name="Canis lupus" total_count="62">
                                                            <taxon self_count="62" tax_id="9615" rank="subspecies" name="Canis lupus familiaris" total_count="62"/>
                                                            </taxon>
                                                            </taxon>
                                                          </taxon>
                                                        </taxon>
                                                      </taxon>
                                                    </taxon>
                                                  </taxon>
                                                </taxon>
                                              </taxon>
                                            </taxon>
                                            <taxon self_count="0" tax_id="8457" name="Sauropsida" total_count="577">
                                              <taxon self_count="0" tax_id="32561" name="Sauria" total_count="577">
                                                <taxon self_count="0" tax_id="1329799" name="Archelosauria" total_count="577">
                                                  <taxon self_count="0" tax_id="8492" name="Archosauria" total_count="577">
                                                    <taxon self_count="0" tax_id="436486" name="Dinosauria" total_count="577">
                                                      <taxon self_count="0" tax_id="436489" name="Saurischia" total_count="577">
                                                        <taxon self_count="0" tax_id="436491" name="Theropoda" total_count="577">
                                                          <taxon self_count="0" tax_id="436492" name="Coelurosauria" total_count="577">
                                                            <taxon self_count="0" tax_id="8782" rank="class" name="Aves" total_count="577">
                                                            <taxon self_count="0" tax_id="8825" rank="superorder" name="Neognathae" total_count="577">
                                                            <taxon self_count="0" tax_id="1549675" name="Galloanserae" total_count="577">
                                                            <taxon self_count="0" tax_id="8976" rank="order" name="Galliformes" total_count="577">
                                                            <taxon self_count="75" tax_id="9005" rank="family" name="Phasianidae" total_count="577">
                                                            <taxon self_count="0" tax_id="9072" rank="subfamily" name="Phasianinae" total_count="501">
                                                            <taxon self_count="0" tax_id="9030" rank="genus" name="Gallus" total_count="501">
                                                            <taxon self_count="501" tax_id="9031" rank="species" name="Gallus gallus" total_count="501"/>
                                                            </taxon>
                                                            </taxon>
                                                            <taxon self_count="0" tax_id="466544" rank="subfamily" name="Perdicinae" total_count="1">
                                                            <taxon self_count="0" tax_id="9090" rank="genus" name="Coturnix" total_count="1">
                                                            <taxon self_count="1" tax_id="93934" rank="species" name="Coturnix japonica" total_count="1"/>
                                                            </taxon>
                                                            </taxon>
                                                            </taxon>
                                                            </taxon>
                                                            </taxon>
                                                            </taxon>
                                                            </taxon>
                                                          </taxon>
                                                        </taxon>
                                                      </taxon>
                                                    </taxon>
                                                  </taxon>
                                                </taxon>
                                              </taxon>
                                            </taxon>
                                          </taxon>
                                        </taxon>
                                      </taxon>
                                    </taxon>
                                  </taxon>
                                </taxon>
                              </taxon>
                            </taxon>
                          </taxon>
                        </taxon>
                      </taxon>
                    </taxon>
                  </taxon>
                </taxon>
                <taxon self_count="0" tax_id="4751" rank="kingdom" name="Fungi" total_count="165">
                  <taxon self_count="0" tax_id="451864" rank="subkingdom" name="Dikarya" total_count="165">
                    <taxon self_count="0" tax_id="4890" rank="phylum" name="Ascomycota" total_count="109">
                      <taxon self_count="0" tax_id="716545" name="saccharomyceta" total_count="109">
                        <taxon self_count="0" tax_id="147537" rank="subphylum" name="Saccharomycotina" total_count="109">
                          <taxon self_count="0" tax_id="4891" rank="class" name="Saccharomycetes" total_count="109">
                            <taxon self_count="0" tax_id="4892" rank="order" name="Saccharomycetales" total_count="109">
                              <taxon self_count="0" tax_id="4893" rank="family" name="Saccharomycetaceae" total_count="109">
                                <taxon self_count="8" tax_id="4930" rank="genus" name="Saccharomyces" total_count="109">
                                  <taxon self_count="0" tax_id="4932" rank="species" name="Saccharomyces cerevisiae" total_count="101">
                                    <taxon self_count="101" tax_id="559292" name="Saccharomyces cerevisiae S288c" total_count="101"/>
                                  </taxon>
                                </taxon>
                              </taxon>
                            </taxon>
                          </taxon>
                        </taxon>
                      </taxon>
                    </taxon>
                    <taxon self_count="0" tax_id="5204" rank="phylum" name="Basidiomycota" total_count="56">
                      <taxon self_count="0" tax_id="452284" rank="subphylum" name="Ustilaginomycotina" total_count="56">
                        <taxon self_count="0" tax_id="1538075" rank="class" name="Malasseziomycetes" total_count="56">
                          <taxon self_count="0" tax_id="162474" rank="order" name="Malasseziales" total_count="56">
                            <taxon self_count="0" tax_id="742845" rank="family" name="Malasseziaceae" total_count="56">
                              <taxon self_count="0" tax_id="55193" rank="genus" name="Malassezia" total_count="56">
                                <taxon self_count="0" tax_id="76773" rank="species" name="Malassezia globosa" total_count="56">
                                  <taxon self_count="56" tax_id="425265" name="Malassezia globosa CBS 7966" total_count="56"/>
                                </taxon>
                              </taxon>
                            </taxon>
                          </taxon>
                        </taxon>
                      </taxon>
                    </taxon>
                  </taxon>
                </taxon>
              </taxon>
              <taxon self_count="0" tax_id="33090" rank="kingdom" name="Viridiplantae" total_count="226">
                <taxon self_count="0" tax_id="35493" rank="phylum" name="Streptophyta" total_count="226">
                  <taxon self_count="0" tax_id="131221" name="Streptophytina" total_count="226">
                    <taxon self_count="1" tax_id="3193" name="Embryophyta" total_count="226">
                      <taxon self_count="0" tax_id="58023" name="Tracheophyta" total_count="225">
                        <taxon self_count="0" tax_id="78536" name="Euphyllophyta" total_count="225">
                          <taxon self_count="4" tax_id="58024" name="Spermatophyta" total_count="225">
                            <taxon self_count="22" tax_id="3398" name="Magnoliophyta" total_count="221">
                              <taxon self_count="60" tax_id="1437183" name="Mesangiospermae" total_count="199">
                                <taxon self_count="0" tax_id="4447" rank="class" name="Liliopsida" total_count="11">
                                  <taxon self_count="0" tax_id="1437197" name="Petrosaviidae" total_count="11">
                                    <taxon self_count="0" tax_id="73496" rank="order" name="Asparagales" total_count="2">
                                      <taxon self_count="0" tax_id="4668" rank="family" name="Amaryllidaceae" total_count="2">
                                        <taxon self_count="0" tax_id="40553" rank="subfamily" name="Allioideae" total_count="2">
                                          <taxon self_count="0" tax_id="703248" rank="tribe" name="Allieae" total_count="2">
                                            <taxon self_count="0" tax_id="4678" rank="genus" name="Allium" total_count="2">
                                              <taxon self_count="2" tax_id="4679" rank="species" name="Allium cepa" total_count="2"/>
                                            </taxon>
                                          </taxon>
                                        </taxon>
                                      </taxon>
                                    </taxon>
                                    <taxon self_count="0" tax_id="4734" rank="subclass" name="commelinids" total_count="9">
                                      <taxon self_count="0" tax_id="38820" rank="order" name="Poales" total_count="9">
                                        <taxon self_count="3" tax_id="4479" rank="family" name="Poaceae" total_count="9">
                                          <taxon self_count="0" tax_id="359160" name="BOP clade" total_count="6">
                                            <taxon self_count="0" tax_id="147368" rank="subfamily" name="Pooideae" total_count="6">
                                              <taxon self_count="0" tax_id="1648038" name="Triticodae" total_count="6">
                                                <taxon self_count="0" tax_id="147389" rank="tribe" name="Triticeae" total_count="6">
                                                  <taxon self_count="6" tax_id="1648030" rank="subtribe" name="Triticinae" total_count="6"/>
                                                </taxon>
                                              </taxon>
                                            </taxon>
                                          </taxon>
                                        </taxon>
                                      </taxon>
                                    </taxon>
                                  </taxon>
                                </taxon>
                                <taxon self_count="0" tax_id="71240" name="eudicotyledons" total_count="128">
                                  <taxon self_count="0" tax_id="91827" name="Gunneridae" total_count="128">
                                    <taxon self_count="0" tax_id="1437201" name="Pentapetalae" total_count="128">
                                      <taxon self_count="3" tax_id="71274" rank="subclass" name="asterids" total_count="21">
                                        <taxon self_count="0" tax_id="91888" name="lamiids" total_count="18">
                                          <taxon self_count="0" tax_id="4069" rank="order" name="Solanales" total_count="18">
                                            <taxon self_count="18" tax_id="4070" rank="family" name="Solanaceae" total_count="18"/>
                                          </taxon>
                                        </taxon>
                                      </taxon>
                                      <taxon self_count="0" tax_id="71275" rank="subclass" name="rosids" total_count="107">
                                        <taxon self_count="0" tax_id="91836" name="malvids" total_count="66">
                                          <taxon self_count="0" tax_id="41938" rank="order" name="Malvales" total_count="27">
                                            <taxon self_count="0" tax_id="3629" rank="family" name="Malvaceae" total_count="27">
                                              <taxon self_count="0" tax_id="214907" rank="subfamily" name="Malvoideae" total_count="27">
                                                <taxon self_count="0" tax_id="3633" rank="genus" name="Gossypium" total_count="27">
                                                  <taxon self_count="27" tax_id="3635" rank="species" name="Gossypium hirsutum" total_count="27"/>
                                                </taxon>
                                              </taxon>
                                            </taxon>
                                          </taxon>
                                          <taxon self_count="0" tax_id="3699" rank="order" name="Brassicales" total_count="32">
                                            <taxon self_count="13" tax_id="3700" rank="family" name="Brassicaceae" total_count="32">
                                              <taxon self_count="0" tax_id="981071" rank="tribe" name="Brassiceae" total_count="19">
                                                <taxon self_count="0" tax_id="3705" rank="genus" name="Brassica" total_count="19">
                                                  <taxon self_count="19" tax_id="3711" rank="species" name="Brassica rapa" total_count="19"/>
                                                </taxon>
                                              </taxon>
                                            </taxon>
                                          </taxon>
                                          <taxon self_count="0" tax_id="41937" rank="order" name="Sapindales" total_count="7">
                                            <taxon self_count="0" tax_id="23513" rank="family" name="Rutaceae" total_count="7">
                                              <taxon self_count="0" tax_id="1728959" rank="subfamily" name="Aurantioideae" total_count="7">
                                                <taxon self_count="7" tax_id="2706" rank="genus" name="Citrus" total_count="7"/>
                                              </taxon>
                                            </taxon>
                                          </taxon>
                                        </taxon>
                                        <taxon self_count="0" tax_id="91835" name="fabids" total_count="41">
                                          <taxon self_count="0" tax_id="72025" rank="order" name="Fabales" total_count="17">
                                            <taxon self_count="0" tax_id="3803" rank="family" name="Fabaceae" total_count="17">
                                              <taxon self_count="4" tax_id="3814" rank="subfamily" name="Papilionoideae" total_count="17">
                                                <taxon self_count="0" tax_id="163722" rank="tribe" name="Cicereae" total_count="13">
                                                  <taxon self_count="0" tax_id="3826" rank="genus" name="Cicer" total_count="13">
                                                    <taxon self_count="13" tax_id="3827" rank="species" name="Cicer arietinum" total_count="13"/>
                                                  </taxon>
                                                </taxon>
                                              </taxon>
                                            </taxon>
                                          </taxon>
                                          <taxon self_count="0" tax_id="71239" rank="order" name="Cucurbitales" total_count="24">
                                            <taxon self_count="0" tax_id="3650" rank="family" name="Cucurbitaceae" total_count="24">
                                              <taxon self_count="0" tax_id="1003877" rank="tribe" name="Benincaseae" total_count="24">
                                                <taxon self_count="0" tax_id="3655" rank="genus" name="Cucumis" total_count="24">
                                                  <taxon self_count="24" tax_id="3656" rank="species" name="Cucumis melo" total_count="24"/>
                                                </taxon>
                                              </taxon>
                                            </taxon>
                                          </taxon>
                                        </taxon>
                                      </taxon>
                                    </taxon>
                                  </taxon>
                                </taxon>
                              </taxon>
                            </taxon>
                          </taxon>
                        </taxon>
                      </taxon>
                    </taxon>
                  </taxon>
                </taxon>
              </taxon>
            </taxon>
            <taxon self_count="4903" tax_id="2" rank="superkingdom" name="Bacteria" total_count="103296">
              <taxon self_count="360" tax_id="1783272" name="Terrabacteria group" total_count="20158">
                <taxon self_count="0" tax_id="201174" rank="phylum" name="Actinobacteria" total_count="17335">
                  <taxon self_count="605" tax_id="1760" rank="class" name="Actinobacteria" total_count="17331">
                    <taxon self_count="0" tax_id="85004" rank="order" name="Bifidobacteriales" total_count="36">
                      <taxon self_count="0" tax_id="31953" rank="family" name="Bifidobacteriaceae" total_count="36">
                        <taxon self_count="1" tax_id="2701" rank="genus" name="Gardnerella" total_count="35">
                          <taxon self_count="32" tax_id="2702" rank="species" name="Gardnerella vaginalis" total_count="34">
                            <taxon self_count="2" tax_id="1261061" name="Gardnerella vaginalis JCP7719" total_count="2"/>
                          </taxon>
                        </taxon>
                        <taxon self_count="0" tax_id="1678" rank="genus" name="Bifidobacterium" total_count="1">
                          <taxon self_count="1" tax_id="1681" rank="species" name="Bifidobacterium bifidum" total_count="1"/>
                        </taxon>
                      </taxon>
                    </taxon>
                    <taxon self_count="0" tax_id="2037" rank="order" name="Actinomycetales" total_count="102">
                      <taxon self_count="6" tax_id="2049" rank="family" name="Actinomycetaceae" total_count="102">
                        <taxon self_count="0" tax_id="76833" rank="genus" name="Actinobaculum" total_count="3">
                          <taxon self_count="3" tax_id="202789" rank="species" name="Actinobaculum massiliense" total_count="3"/>
                        </taxon>
                        <taxon self_count="81" tax_id="1654" rank="genus" name="Actinomyces" total_count="89">
                          <taxon self_count="3" tax_id="52773" rank="species" name="Actinomyces meyeri" total_count="3"/>
                          <taxon self_count="0" tax_id="712121" rank="species" name="Actinomyces sp. oral taxon 181" total_count="2">
                            <taxon self_count="2" tax_id="1127690" name="Actinomyces sp. oral taxon 181 str. F0379" total_count="2"/>
                          </taxon>
                          <taxon self_count="3" tax_id="33007" rank="species" name="Actinomyces neuii" total_count="3"/>
                        </taxon>
                        <taxon self_count="0" tax_id="1522056" rank="genus" name="Flaviflexus" total_count="4">
                          <taxon self_count="4" tax_id="1522309" rank="species" name="Flaviflexus sp. SIT4" total_count="4"/>
                        </taxon>
                      </taxon>
                    </taxon>
                    <taxon self_count="77" tax_id="85006" rank="order" name="Micrococcales" total_count="1463">
                      <taxon self_count="0" tax_id="85023" rank="family" name="Microbacteriaceae" total_count="71">
                        <taxon self_count="69" tax_id="33882" rank="genus" name="Microbacterium" total_count="71">
                          <taxon self_count="2" tax_id="1263625" rank="species" name="Microbacterium sp. SA39" total_count="2"/>
                        </taxon>
                      </taxon>
                      <taxon self_count="0" tax_id="85020" rank="family" name="Dermabacteraceae" total_count="43">
                        <taxon self_count="38" tax_id="43668" rank="genus" name="Brachybacterium" total_count="43">
                          <taxon self_count="5" tax_id="1704590" rank="species" name="Brachybacterium sp. SW0106-09" total_count="5"/>
                        </taxon>
                      </taxon>
                      <taxon self_count="0" tax_id="1268" rank="family" name="Micrococcaceae" total_count="1155">
                        <taxon self_count="49" tax_id="57493" rank="genus" name="Kocuria" total_count="370">
                          <taxon self_count="14" tax_id="71999" rank="species" name="Kocuria palustris" total_count="17">
                            <taxon self_count="3" tax_id="1236550" name="Kocuria palustris PEL" total_count="3"/>
                          </taxon>
                          <taxon self_count="303" tax_id="72000" rank="species" name="Kocuria rhizophila" total_count="303"/>
                          <taxon self_count="1" tax_id="37923" rank="species" name="Kocuria kristinae" total_count="1"/>
                        </taxon>
                        <taxon self_count="33" tax_id="32207" rank="genus" name="Rothia" total_count="194">
                          <taxon self_count="161" tax_id="43675" rank="species" name="Rothia mucilaginosa" total_count="161"/>
                        </taxon>
                        <taxon self_count="461" tax_id="1269" rank="genus" name="Micrococcus" total_count="591">
                          <taxon self_count="130" tax_id="1270" rank="species" name="Micrococcus luteus" total_count="130"/>
                        </taxon>
                      </taxon>
                      <taxon self_count="0" tax_id="145357" rank="family" name="Dermacoccaceae" total_count="104">
                        <taxon self_count="97" tax_id="57495" rank="genus" name="Dermacoccus" total_count="97"/>
                        <taxon self_count="0" tax_id="57499" rank="genus" name="Kytococcus" total_count="7">
                          <taxon self_count="0" tax_id="1276" rank="species" name="Kytococcus sedentarius" total_count="7">
                            <taxon self_count="7" tax_id="478801" name="Kytococcus sedentarius DSM 20547" total_count="7"/>
                          </taxon>
                        </taxon>
                      </taxon>
                      <taxon self_count="0" tax_id="85021" rank="family" name="Intrasporangiaceae" total_count="7">
                        <taxon self_count="0" tax_id="53457" rank="genus" name="Janibacter" total_count="7">
                          <taxon self_count="0" tax_id="364298" rank="species" name="Janibacter hoylei" total_count="7">
                            <taxon self_count="7" tax_id="1210046" name="Janibacter hoylei PVAS-1" total_count="7"/>
                          </taxon>
                        </taxon>
                      </taxon>
                      <taxon self_count="0" tax_id="85019" rank="family" name="Brevibacteriaceae" total_count="6">
                        <taxon self_count="0" tax_id="1696" rank="genus" name="Brevibacterium" total_count="6">
                          <taxon self_count="0" tax_id="33889" rank="species" name="Brevibacterium casei" total_count="6">
                            <taxon self_count="6" tax_id="1229781" name="Brevibacterium casei S18" total_count="6"/>
                          </taxon>
                        </taxon>
                      </taxon>
                    </taxon>
                    <taxon self_count="0" tax_id="85007" rank="order" name="Corynebacteriales" total_count="1060">
                      <taxon self_count="0" tax_id="85029" rank="family" name="Dietziaceae" total_count="15">
                        <taxon self_count="15" tax_id="37914" rank="genus" name="Dietzia" total_count="15"/>
                      </taxon>
                      <taxon self_count="0" tax_id="1762" rank="family" name="Mycobacteriaceae" total_count="86">
                        <taxon self_count="67" tax_id="1763" rank="genus" name="Mycobacterium" total_count="86">
                          <taxon self_count="14" tax_id="670516" rank="species group" name="Mycobacterium chelonae group" total_count="19">
                            <taxon self_count="5" tax_id="83262" rank="species" name="Mycobacterium immunogenum" total_count="5"/>
                          </taxon>
                        </taxon>
                      </taxon>
                      <taxon self_count="0" tax_id="85025" rank="family" name="Nocardiaceae" total_count="337">
                        <taxon self_count="333" tax_id="1827" rank="genus" name="Rhodococcus" total_count="337">
                          <taxon self_count="4" tax_id="1449068" rank="species" name="Rhodococcus sp. UNC23MFCrub1.1" total_count="4"/>
                        </taxon>
                      </taxon>
                      <taxon self_count="12" tax_id="1653" rank="family" name="Corynebacteriaceae" total_count="622">
                        <taxon self_count="230" tax_id="1716" rank="genus" name="Corynebacterium" total_count="257">
                          <taxon self_count="1" tax_id="401472" rank="species" name="Corynebacterium ureicelerivorans" total_count="1"/>
                          <taxon self_count="16" tax_id="43768" rank="species" name="Corynebacterium matruchotii" total_count="16"/>
                          <taxon self_count="9" tax_id="156978" rank="species" name="Corynebacterium imitans" total_count="9"/>
                          <taxon self_count="0" tax_id="169292" rank="species" name="Corynebacterium aurimucosum" total_count="1">
                            <taxon self_count="1" tax_id="548476" name="Corynebacterium aurimucosum ATCC 700975" total_count="1"/>
                          </taxon>
                        </taxon>
                        <taxon self_count="0" tax_id="144193" rank="genus" name="Turicella" total_count="353">
                          <taxon self_count="353" tax_id="29321" rank="species" name="Turicella otitidis" total_count="353"/>
                        </taxon>
                      </taxon>
                    </taxon>
                    <taxon self_count="0" tax_id="85008" rank="order" name="Micromonosporales" total_count="1">
                      <taxon self_count="0" tax_id="28056" rank="family" name="Micromonosporaceae" total_count="1">
                        <taxon self_count="0" tax_id="195964" rank="genus" name="Asanoa" total_count="1">
                          <taxon self_count="1" tax_id="53367" rank="species" name="Asanoa ferruginea" total_count="1"/>
                        </taxon>
                      </taxon>
                    </taxon>
                    <taxon self_count="0" tax_id="85009" rank="order" name="Propionibacteriales" total_count="14064">
                      <taxon self_count="0" tax_id="85015" rank="family" name="Nocardioidaceae" total_count="6">
                        <taxon self_count="0" tax_id="1839" rank="genus" name="Nocardioides" total_count="2">
                          <taxon self_count="0" tax_id="433660" rank="species" name="Nocardioides halotolerans" total_count="2">
                            <taxon self_count="2" tax_id="1122609" name="Nocardioides halotolerans DSM 19273" total_count="2"/>
                          </taxon>
                        </taxon>
                        <taxon self_count="4" tax_id="2040" rank="genus" name="Aeromicrobium" total_count="4"/>
                      </taxon>
                      <taxon self_count="0" tax_id="31957" rank="family" name="Propionibacteriaceae" total_count="14058">
                        <taxon self_count="13643" tax_id="1743" rank="genus" name="Propionibacterium" total_count="14058">
                          <taxon self_count="227" tax_id="1747" rank="species" name="Propionibacterium acnes" total_count="232">
                            <taxon self_count="5" tax_id="1234380" name="Propionibacterium acnes C1" total_count="5"/>
                          </taxon>
                          <taxon self_count="154" tax_id="1050843" rank="species" name="Propionibacterium humerusii" total_count="154"/>
                          <taxon self_count="29" tax_id="1203573" rank="species" name="Propionibacterium sp. KPL1844" total_count="29"/>
                        </taxon>
                      </taxon>
                    </taxon>
                  </taxon>
                  <taxon self_count="0" tax_id="84998" rank="class" name="Coriobacteriia" total_count="4">
                    <taxon self_count="0" tax_id="84999" rank="order" name="Coriobacteriales" total_count="4">
                      <taxon self_count="2" tax_id="84107" rank="family" name="Coriobacteriaceae" total_count="4">
                        <taxon self_count="2" tax_id="102106" rank="genus" name="Collinsella" total_count="2"/>
                      </taxon>
                    </taxon>
                  </taxon>
                </taxon>
                <taxon self_count="88" tax_id="1239" rank="phylum" name="Firmicutes" total_count="2463">
                  <taxon self_count="178" tax_id="91061" rank="class" name="Bacilli" total_count="2256">
                    <taxon self_count="21" tax_id="1385" rank="order" name="Bacillales" total_count="747">
                      <taxon self_count="0" tax_id="186817" rank="family" name="Bacillaceae" total_count="73">
                        <taxon self_count="0" tax_id="129337" rank="genus" name="Geobacillus" total_count="3">
                          <taxon self_count="3" tax_id="153151" rank="species" name="Geobacillus toebii" total_count="3"/>
                        </taxon>
                        <taxon self_count="70" tax_id="1386" rank="genus" name="Bacillus" total_count="70"/>
                      </taxon>
                      <taxon self_count="0" tax_id="186822" rank="family" name="Paenibacillaceae" total_count="8">
                        <taxon self_count="0" tax_id="44249" rank="genus" name="Paenibacillus" total_count="8">
                          <taxon self_count="0" tax_id="1333845" rank="species" name="Paenibacillus sophorae" total_count="8">
                            <taxon self_count="8" tax_id="682957" name="Paenibacillus sophorae S27" total_count="8"/>
                          </taxon>
                        </taxon>
                      </taxon>
                      <taxon self_count="0" tax_id="90964" rank="family" name="Staphylococcaceae" total_count="605">
                        <taxon self_count="413" tax_id="1279" rank="genus" name="Staphylococcus" total_count="603">
                          <taxon self_count="39" tax_id="1280" rank="species" name="Staphylococcus aureus" total_count="39"/>
                          <taxon self_count="72" tax_id="1282" rank="species" name="Staphylococcus epidermidis" total_count="72"/>
                          <taxon self_count="79" tax_id="1286" rank="species" name="Staphylococcus simulans" total_count="79"/>
                        </taxon>
                        <taxon self_count="2" tax_id="45669" rank="genus" name="Salinicoccus" total_count="2"/>
                      </taxon>
                      <taxon self_count="0" tax_id="539002" name="Bacillales incertae sedis" total_count="40">
                        <taxon self_count="0" tax_id="539738" name="Bacillales Family XI. Incertae Sedis" total_count="40">
                          <taxon self_count="2" tax_id="1378" rank="genus" name="Gemella" total_count="40">
                            <taxon self_count="15" tax_id="1379" rank="species" name="Gemella haemolysans" total_count="29">
                              <taxon self_count="6" tax_id="562981" name="Gemella haemolysans M341" total_count="6"/>
                              <taxon self_count="8" tax_id="546270" name="Gemella haemolysans ATCC 10379" total_count="8"/>
                            </taxon>
                            <taxon self_count="7" tax_id="84135" rank="species" name="Gemella sanguinis" total_count="9">
                              <taxon self_count="2" tax_id="562983" name="Gemella sanguinis M325" total_count="2"/>
                            </taxon>
                          </taxon>
                        </taxon>
                      </taxon>
                    </taxon>
                    <taxon self_count="19" tax_id="186826" rank="order" name="Lactobacillales" total_count="1331">
                      <taxon self_count="0" tax_id="1300" rank="family" name="Streptococcaceae" total_count="1199">
                        <taxon self_count="952" tax_id="1301" rank="genus" name="Streptococcus" total_count="1125">
                          <taxon self_count="39" tax_id="28037" rank="species" name="Streptococcus mitis" total_count="51">
                            <taxon self_count="1" tax_id="1159208" name="Streptococcus mitis SPAR10" total_count="1"/>
                            <taxon self_count="0" tax_id="134262" name="Streptococcus mitis bv. 2" total_count="1">
                              <taxon self_count="1" tax_id="1000588" name="Streptococcus mitis bv. 2 str. SK95" total_count="1"/>
                            </taxon>
                            <taxon self_count="1" tax_id="1415765" name="Streptococcus mitis 21/39" total_count="1"/>
                            <taxon self_count="4" tax_id="1008453" name="Streptococcus mitis SK1080" total_count="4"/>
                            <taxon self_count="1" tax_id="864567" name="Streptococcus mitis ATCC 6249" total_count="1"/>
                            <taxon self_count="4" tax_id="585204" name="Streptococcus mitis SK597" total_count="4"/>
                          </taxon>
                          <taxon self_count="8" tax_id="435842" rank="species" name="Streptococcus sp. C150" total_count="8"/>
                          <taxon self_count="0" tax_id="119603" rank="species group" name="Streptococcus dysgalactiae group" total_count="2">
                            <taxon self_count="0" tax_id="1334" rank="species" name="Streptococcus dysgalactiae" total_count="2">
                              <taxon self_count="0" tax_id="119602" rank="subspecies" name="Streptococcus dysgalactiae subsp. equisimilis" total_count="2">
                                <taxon self_count="2" tax_id="617121" name="Streptococcus dysgalactiae subsp. equisimilis RE378" total_count="2"/>
                              </taxon>
                            </taxon>
                          </taxon>
                          <taxon self_count="2" tax_id="1156433" rank="species" name="Streptococcus sp. I-P16" total_count="2"/>
                          <taxon self_count="29" tax_id="1308" rank="species" name="Streptococcus thermophilus" total_count="29"/>
                          <taxon self_count="25" tax_id="1313" rank="species" name="Streptococcus pneumoniae" total_count="25"/>
                          <taxon self_count="25" tax_id="1318" rank="species" name="Streptococcus parasanguinis" total_count="25"/>
                          <taxon self_count="1" tax_id="1579342" rank="species" name="Streptococcus sp. 343_SSPC" total_count="1"/>
                          <taxon self_count="2" tax_id="1156431" rank="species" name="Streptococcus sp. I-G2" total_count="2"/>
                          <taxon self_count="0" tax_id="1343" rank="species" name="Streptococcus vestibularis" total_count="1">
                            <taxon self_count="1" tax_id="889206" name="Streptococcus vestibularis ATCC 49124" total_count="1"/>
                          </taxon>
                          <taxon self_count="12" tax_id="1305" rank="species" name="Streptococcus sanguinis" total_count="12"/>
                          <taxon self_count="0" tax_id="68891" rank="species" name="Streptococcus peroris" total_count="15">
                            <taxon self_count="15" tax_id="888746" name="Streptococcus peroris ATCC 700780" total_count="15"/>
                          </taxon>
                        </taxon>
                        <taxon self_count="0" tax_id="1357" rank="genus" name="Lactococcus" total_count="74">
                          <taxon self_count="74" tax_id="1358" rank="species" name="Lactococcus lactis" total_count="74"/>
                        </taxon>
                      </taxon>
                      <taxon self_count="0" tax_id="33958" rank="family" name="Lactobacillaceae" total_count="98">
                        <taxon self_count="62" tax_id="1578" rank="genus" name="Lactobacillus" total_count="98">
                          <taxon self_count="5" tax_id="1596" rank="species" name="Lactobacillus gasseri" total_count="5"/>
                          <taxon self_count="31" tax_id="47770" rank="species" name="Lactobacillus crispatus" total_count="31"/>
                        </taxon>
                      </taxon>
                      <taxon self_count="0" tax_id="81850" rank="family" name="Leuconostocaceae" total_count="1">
                        <taxon self_count="0" tax_id="1243" rank="genus" name="Leuconostoc" total_count="1">
                          <taxon self_count="1" tax_id="33968" rank="species" name="Leuconostoc pseudomesenteroides" total_count="1"/>
                        </taxon>
                      </taxon>
                      <taxon self_count="0" tax_id="186828" rank="family" name="Carnobacteriaceae" total_count="11">
                        <taxon self_count="0" tax_id="117563" rank="genus" name="Granulicatella" total_count="11">
                          <taxon self_count="0" tax_id="137732" rank="species" name="Granulicatella elegans" total_count="11">
                            <taxon self_count="11" tax_id="626369" name="Granulicatella elegans ATCC 700633" total_count="11"/>
                          </taxon>
                        </taxon>
                      </taxon>
                      <taxon self_count="0" tax_id="186827" rank="family" name="Aerococcaceae" total_count="3">
                        <taxon self_count="0" tax_id="66831" rank="genus" name="Facklamia" total_count="3">
                          <taxon self_count="0" tax_id="137730" rank="species" name="Facklamia ignava" total_count="3">
                            <taxon self_count="3" tax_id="883112" name="Facklamia ignava CCUG 37419" total_count="3"/>
                          </taxon>
                        </taxon>
                      </taxon>
                    </taxon>
                  </taxon>
                  <taxon self_count="0" tax_id="909932" rank="class" name="Negativicutes" total_count="27">
                    <taxon self_count="0" tax_id="909929" rank="order" name="Selenomonadales" total_count="3">
                      <taxon self_count="0" tax_id="1843490" rank="family" name="Sporomusaceae" total_count="3">
                        <taxon self_count="0" tax_id="112902" rank="genus" name="Propionispora" total_count="3">
                          <taxon self_count="3" tax_id="1677858" rank="species" name="Propionispora sp. Iso2/2" total_count="3"/>
                        </taxon>
                      </taxon>
                    </taxon>
                    <taxon self_count="0" tax_id="1843489" rank="order" name="Veillonellales" total_count="24">
                      <taxon self_count="1" tax_id="31977" rank="family" name="Veillonellaceae" total_count="24">
                        <taxon self_count="23" tax_id="29465" rank="genus" name="Veillonella" total_count="23"/>
                      </taxon>
                    </taxon>
                  </taxon>
                  <taxon self_count="0" tax_id="1737404" rank="class" name="Tissierellia" total_count="80">
                    <taxon self_count="0" tax_id="1737405" rank="order" name="Tissierellales" total_count="80">
                      <taxon self_count="7" tax_id="1570339" rank="family" name="Peptoniphilaceae" total_count="80">
                        <taxon self_count="0" tax_id="165779" rank="genus" name="Anaerococcus" total_count="18">
                          <taxon self_count="0" tax_id="33029" rank="species" name="Anaerococcus hydrogenalis" total_count="3">
                            <taxon self_count="3" tax_id="879306" name="Anaerococcus hydrogenalis ACS-025-V-Sch4" total_count="3"/>
                          </taxon>
                          <taxon self_count="0" tax_id="1288120" rank="species" name="Anaerococcus senegalensis" total_count="15">
                            <taxon self_count="15" tax_id="1033733" name="Anaerococcus senegalensis JC48" total_count="15"/>
                          </taxon>
                        </taxon>
                        <taxon self_count="0" tax_id="150022" rank="genus" name="Finegoldia" total_count="37">
                          <taxon self_count="25" tax_id="1260" rank="species" name="Finegoldia magna" total_count="37">
                            <taxon self_count="12" tax_id="525282" name="Finegoldia magna ATCC 53516" total_count="12"/>
                          </taxon>
                        </taxon>
                        <taxon self_count="0" tax_id="162289" rank="genus" name="Peptoniphilus" total_count="18">
                          <taxon self_count="4" tax_id="54005" rank="species" name="Peptoniphilus harei" total_count="4"/>
                          <taxon self_count="0" tax_id="1175452" rank="species" name="Peptoniphilus rhinitidis" total_count="14">
                            <taxon self_count="14" tax_id="875454" name="Peptoniphilus rhinitidis 1-13" total_count="14"/>
                          </taxon>
                        </taxon>
                      </taxon>
                    </taxon>
                  </taxon>
                  <taxon self_count="0" tax_id="186801" rank="class" name="Clostridia" total_count="11">
                    <taxon self_count="10" tax_id="186802" rank="order" name="Clostridiales" total_count="11">
                      <taxon self_count="1" tax_id="31979" rank="family" name="Clostridiaceae" total_count="1"/>
                    </taxon>
                  </taxon>
                  <taxon self_count="0" tax_id="526524" rank="class" name="Erysipelotrichia" total_count="1">
                    <taxon self_count="0" tax_id="526525" rank="order" name="Erysipelotrichales" total_count="1">
                      <taxon self_count="0" tax_id="128827" rank="family" name="Erysipelotrichaceae" total_count="1">
                        <taxon self_count="0" tax_id="123375" rank="genus" name="Solobacterium" total_count="1">
                          <taxon self_count="0" tax_id="102148" rank="species" name="Solobacterium moorei" total_count="1">
                            <taxon self_count="1" tax_id="706433" name="Solobacterium moorei F0204" total_count="1"/>
                          </taxon>
                        </taxon>
                      </taxon>
                    </taxon>
                  </taxon>
                </taxon>
              </taxon>
              <taxon self_count="1892" tax_id="1224" rank="phylum" name="Proteobacteria" total_count="77995">
                <taxon self_count="66" tax_id="28216" rank="class" name="Betaproteobacteria" total_count="1453">
                  <taxon self_count="1" tax_id="80840" rank="order" name="Burkholderiales" total_count="1192">
                    <taxon self_count="526" tax_id="80864" rank="family" name="Comamonadaceae" total_count="1071">
                      <taxon self_count="128" tax_id="12916" rank="genus" name="Acidovorax" total_count="398">
                        <taxon self_count="1" tax_id="512030" rank="species" name="Acidovorax sp. NO-1" total_count="1"/>
                        <taxon self_count="2" tax_id="80869" rank="species" name="Acidovorax citrulli" total_count="2"/>
                        <taxon self_count="46" tax_id="343013" rank="species" name="Acidovorax caeni" total_count="46"/>
                        <taxon self_count="221" tax_id="80878" rank="species" name="Acidovorax temperans" total_count="221"/>
                      </taxon>
                      <taxon self_count="0" tax_id="238749" rank="genus" name="Diaphorobacter" total_count="32">
                        <taxon self_count="32" tax_id="680496" rank="species" name="Diaphorobacter sp. J5-51" total_count="32"/>
                      </taxon>
                      <taxon self_count="115" tax_id="80865" rank="genus" name="Delftia" total_count="115"/>
                    </taxon>
                    <taxon self_count="0" tax_id="75682" rank="family" name="Oxalobacteraceae" total_count="8">
                      <taxon self_count="8" tax_id="149698" rank="genus" name="Massilia" total_count="8"/>
                    </taxon>
                    <taxon self_count="0" tax_id="119065" name="unclassified Burkholderiales" total_count="37">
                      <taxon self_count="0" tax_id="224471" name="Burkholderiales Genera incertae sedis" total_count="37">
                        <taxon self_count="0" tax_id="114248" rank="genus" name="Tepidimonas" total_count="36">
                          <taxon self_count="36" tax_id="307486" rank="species" name="Tepidimonas taiwanensis" total_count="36"/>
                        </taxon>
                        <taxon self_count="1" tax_id="316612" rank="genus" name="Methylibium" total_count="1"/>
                      </taxon>
                    </taxon>
                    <taxon self_count="31" tax_id="119060" rank="family" name="Burkholderiaceae" total_count="75">
                      <taxon self_count="0" tax_id="47670" rank="genus" name="Lautropia" total_count="13">
                        <taxon self_count="0" tax_id="47671" rank="species" name="Lautropia mirabilis" total_count="13">
                          <taxon self_count="13" tax_id="887898" name="Lautropia mirabilis ATCC 51599" total_count="13"/>
                        </taxon>
                      </taxon>
                      <taxon self_count="0" tax_id="48736" rank="genus" name="Ralstonia" total_count="31">
                        <taxon self_count="31" tax_id="329" rank="species" name="Ralstonia pickettii" total_count="31"/>
                      </taxon>
                    </taxon>
                  </taxon>
                  <taxon self_count="0" tax_id="206351" rank="order" name="Neisseriales" total_count="113">
                    <taxon self_count="10" tax_id="481" rank="family" name="Neisseriaceae" total_count="109">
                      <taxon self_count="89" tax_id="482" rank="genus" name="Neisseria" total_count="99">
                        <taxon self_count="4" tax_id="1581124" rank="species" name="Neisseria sp. HMSC06F02" total_count="4"/>
                        <taxon self_count="0" tax_id="490" rank="species" name="Neisseria sicca" total_count="3">
                          <taxon self_count="3" tax_id="1095748" name="Neisseria sicca VK64" total_count="3"/>
                        </taxon>
                        <taxon self_count="0" tax_id="483" rank="species" name="Neisseria cinerea" total_count="3">
                          <taxon self_count="3" tax_id="546262" name="Neisseria cinerea ATCC 14685" total_count="3"/>
                        </taxon>
                      </taxon>
                    </taxon>
                    <taxon self_count="0" tax_id="1499392" rank="family" name="Chromobacteriaceae" total_count="4">
                      <taxon self_count="4" tax_id="397456" rank="genus" name="Gulbenkiania" total_count="4"/>
                    </taxon>
                  </taxon>
                  <taxon self_count="0" tax_id="119069" rank="order" name="Hydrogenophilales" total_count="46">
                    <taxon self_count="0" tax_id="206349" rank="family" name="Hydrogenophilaceae" total_count="46">
                      <taxon self_count="0" tax_id="203470" rank="genus" name="Tepidiphilus" total_count="46">
                        <taxon self_count="46" tax_id="876478" rank="species" name="Tepidiphilus thermophilus" total_count="46"/>
                      </taxon>
                    </taxon>
                  </taxon>
                  <taxon self_count="0" tax_id="206389" rank="order" name="Rhodocyclales" total_count="36">
                    <taxon self_count="0" tax_id="75787" rank="family" name="Rhodocyclaceae" total_count="36">
                      <taxon self_count="0" tax_id="73029" rank="genus" name="Dechloromonas" total_count="36">
                        <taxon self_count="0" tax_id="73030" rank="species" name="Dechloromonas agitata" total_count="36">
                          <taxon self_count="36" tax_id="1304883" name="Dechloromonas agitata is5" total_count="36"/>
                        </taxon>
                      </taxon>
                    </taxon>
                  </taxon>
                </taxon>
                <taxon self_count="54612" tax_id="1236" rank="class" name="Gammaproteobacteria" total_count="73821">
                  <taxon self_count="0" tax_id="91347" rank="order" name="Enterobacteriales" total_count="13662">
                    <taxon self_count="10364" tax_id="543" rank="family" name="Enterobacteriaceae" total_count="13662">
                      <taxon self_count="34" tax_id="544" rank="genus" name="Citrobacter" total_count="34"/>
                      <taxon self_count="0" tax_id="1330547" rank="genus" name="Kosakonia" total_count="1">
                        <taxon self_count="1" tax_id="283686" rank="species" name="Kosakonia radicincitans" total_count="1"/>
                      </taxon>
                      <taxon self_count="107" tax_id="570" rank="genus" name="Klebsiella" total_count="107"/>
                      <taxon self_count="116" tax_id="53335" rank="genus" name="Pantoea" total_count="134">
                        <taxon self_count="18" tax_id="470934" rank="species" name="Pantoea vagans" total_count="18"/>
                      </taxon>
                      <taxon self_count="2222" tax_id="613" rank="genus" name="Serratia" total_count="3019">
                        <taxon self_count="633" tax_id="615" rank="species" name="Serratia marcescens" total_count="778">
                          <taxon self_count="73" tax_id="435998" name="Serratia marcescens WW4" total_count="73"/>
                          <taxon self_count="72" tax_id="1357297" name="Serratia marcescens EGD-HP20" total_count="72"/>
                        </taxon>
                        <taxon self_count="19" tax_id="1327989" rank="species" name="Serratia sp. FS14" total_count="19"/>
                      </taxon>
                      <taxon self_count="0" tax_id="547" rank="genus" name="Enterobacter" total_count="3">
                        <taxon self_count="0" tax_id="354276" rank="species group" name="Enterobacter cloacae complex" total_count="3">
                          <taxon self_count="3" tax_id="550" rank="species" name="Enterobacter cloacae" total_count="3"/>
                        </taxon>
                      </taxon>
                    </taxon>
                  </taxon>
                  <taxon self_count="0" tax_id="72274" rank="order" name="Pseudomonadales" total_count="5030">
                    <taxon self_count="0" tax_id="468" rank="family" name="Moraxellaceae" total_count="1510">
                      <taxon self_count="1026" tax_id="469" rank="genus" name="Acinetobacter" total_count="1506">
                        <taxon self_count="7" tax_id="1795629" rank="species" name="Acinetobacter sp. BMW17" total_count="7"/>
                        <taxon self_count="1" tax_id="1217704" rank="species" name="Acinetobacter sp. NIPH 284" total_count="1"/>
                        <taxon self_count="75" tax_id="756892" rank="species" name="Acinetobacter indicus" total_count="75"/>
                        <taxon self_count="62" tax_id="909768" rank="species group" name="Acinetobacter calcoaceticus/baumannii complex" total_count="62"/>
                        <taxon self_count="1" tax_id="202954" rank="species" name="Acinetobacter tandoii" total_count="1"/>
                        <taxon self_count="334" tax_id="40215" rank="species" name="Acinetobacter junii" total_count="334"/>
                      </taxon>
                      <taxon self_count="0" tax_id="475" rank="genus" name="Moraxella" total_count="4">
                        <taxon self_count="0" tax_id="46226" rank="subgenus" name="Branhamella" total_count="4">
                          <taxon self_count="4" tax_id="480" rank="species" name="Moraxella catarrhalis" total_count="4"/>
                        </taxon>
                      </taxon>
                    </taxon>
                    <taxon self_count="0" tax_id="135621" rank="family" name="Pseudomonadaceae" total_count="3520">
                      <taxon self_count="3087" tax_id="286" rank="genus" name="Pseudomonas" total_count="3520">
                        <taxon self_count="8" tax_id="1125977" rank="species" name="Pseudomonas sp. PAMC 25886" total_count="8"/>
                        <taxon self_count="37" tax_id="136846" rank="species group" name="Pseudomonas stutzeri group" total_count="118">
                          <taxon self_count="0" tax_id="578833" rank="species subgroup" name="Pseudomonas stutzeri subgroup" total_count="81">
                            <taxon self_count="81" tax_id="316" rank="species" name="Pseudomonas stutzeri" total_count="81"/>
                          </taxon>
                        </taxon>
                        <taxon self_count="49" tax_id="1197727" rank="species" name="Pseudomonas sp. Ag1" total_count="49"/>
                        <taxon self_count="17" tax_id="1661046" rank="species" name="Pseudomonas sp. NBRC 111131" total_count="17"/>
                        <taxon self_count="3" tax_id="1230461" rank="species" name="Pseudomonas sp. ABAC61" total_count="3"/>
                        <taxon self_count="41" tax_id="136843" rank="species group" name="Pseudomonas fluorescens group" total_count="47">
                          <taxon self_count="0" tax_id="75612" rank="species" name="Pseudomonas mandelii" total_count="6">
                            <taxon self_count="6" tax_id="1147786" name="Pseudomonas mandelii JR-1" total_count="6"/>
                          </taxon>
                        </taxon>
                        <taxon self_count="0" tax_id="136841" rank="species group" name="Pseudomonas aeruginosa group" total_count="191">
                          <taxon self_count="84" tax_id="287" rank="species" name="Pseudomonas aeruginosa" total_count="84"/>
                          <taxon self_count="0" tax_id="1232139" rank="species subgroup" name="Pseudomonas oleovorans/pseudoalcaligenes group" total_count="107">
                            <taxon self_count="107" tax_id="330" rank="species" name="Pseudomonas pseudoalcaligenes" total_count="107"/>
                          </taxon>
                        </taxon>
                      </taxon>
                    </taxon>
                  </taxon>
                  <taxon self_count="0" tax_id="135625" rank="order" name="Pasteurellales" total_count="161">
                    <taxon self_count="21" tax_id="712" rank="family" name="Pasteurellaceae" total_count="161">
                      <taxon self_count="118" tax_id="724" rank="genus" name="Haemophilus" total_count="135">
                        <taxon self_count="8" tax_id="726" rank="species" name="Haemophilus haemolyticus" total_count="8"/>
                        <taxon self_count="0" tax_id="735" rank="species" name="Haemophilus parahaemolyticus" total_count="6">
                          <taxon self_count="1" tax_id="1430896" name="Haemophilus parahaemolyticus G321" total_count="1"/>
                          <taxon self_count="5" tax_id="1095744" name="Haemophilus parahaemolyticus HK385" total_count="5"/>
                        </taxon>
                        <taxon self_count="0" tax_id="1078480" rank="species" name="Haemophilus sputorum" total_count="3">
                          <taxon self_count="3" tax_id="1035839" name="Haemophilus sputorum CCUG 13788" total_count="3"/>
                        </taxon>
                      </taxon>
                      <taxon self_count="0" tax_id="416916" rank="genus" name="Aggregatibacter" total_count="5">
                        <taxon self_count="4" tax_id="732" rank="species" name="Aggregatibacter aphrophilus" total_count="4"/>
                        <taxon self_count="0" tax_id="712148" rank="species" name="Aggregatibacter sp. oral taxon 458" total_count="1">
                          <taxon self_count="1" tax_id="1321772" name="Aggregatibacter sp. oral taxon 458 str. W10330" total_count="1"/>
                        </taxon>
                      </taxon>
                    </taxon>
                  </taxon>
                  <taxon self_count="0" tax_id="135614" rank="order" name="Xanthomonadales" total_count="355">
                    <taxon self_count="0" tax_id="32033" rank="family" name="Xanthomonadaceae" total_count="355">
                      <taxon self_count="67" tax_id="40323" rank="genus" name="Stenotrophomonas" total_count="217">
                        <taxon self_count="0" tax_id="995085" name="Stenotrophomonas maltophilia group" total_count="150">
                          <taxon self_count="150" tax_id="40324" rank="species" name="Stenotrophomonas maltophilia" total_count="150"/>
                        </taxon>
                      </taxon>
                      <taxon self_count="37" tax_id="338" rank="genus" name="Xanthomonas" total_count="138">
                        <taxon self_count="101" tax_id="339" rank="species" name="Xanthomonas campestris" total_count="101"/>
                      </taxon>
                    </taxon>
                  </taxon>
                  <taxon self_count="0" tax_id="135624" rank="order" name="Aeromonadales" total_count="1">
                    <taxon self_count="0" tax_id="84642" rank="family" name="Aeromonadaceae" total_count="1">
                      <taxon self_count="0" tax_id="642" rank="genus" name="Aeromonas" total_count="1">
                        <taxon self_count="1" tax_id="29489" rank="species" name="Aeromonas enteropelogenes" total_count="1"/>
                      </taxon>
                    </taxon>
                  </taxon>
                </taxon>
                <taxon self_count="186" tax_id="28211" rank="class" name="Alphaproteobacteria" total_count="827">
                  <taxon self_count="0" tax_id="204455" rank="order" name="Rhodobacterales" total_count="108">
                    <taxon self_count="0" tax_id="31989" rank="family" name="Rhodobacteraceae" total_count="108">
                      <taxon self_count="43" tax_id="227873" rank="genus" name="Pannonibacter" total_count="105">
                        <taxon self_count="62" tax_id="466044" rank="species" name="Pannonibacter indicus" total_count="62"/>
                      </taxon>
                      <taxon self_count="0" tax_id="265" rank="genus" name="Paracoccus" total_count="3">
                        <taxon self_count="0" tax_id="147645" rank="species" name="Paracoccus yeei" total_count="3">
                          <taxon self_count="3" tax_id="1446473" name="Paracoccus yeei ATCC BAA-599" total_count="3"/>
                        </taxon>
                      </taxon>
                    </taxon>
                  </taxon>
                  <taxon self_count="0" tax_id="204441" rank="order" name="Rhodospirillales" total_count="146">
                    <taxon self_count="0" tax_id="451274" name="unclassified Rhodospirillales" total_count="19">
                      <taxon self_count="0" tax_id="212791" rank="genus" name="Enhydrobacter" total_count="19">
                        <taxon self_count="19" tax_id="225324" rank="species" name="Enhydrobacter aerosaccus" total_count="19"/>
                      </taxon>
                    </taxon>
                    <taxon self_count="115" tax_id="433" rank="family" name="Acetobacteraceae" total_count="127">
                      <taxon self_count="12" tax_id="125216" rank="genus" name="Roseomonas" total_count="12"/>
                    </taxon>
                  </taxon>
                  <taxon self_count="0" tax_id="766" rank="order" name="Rickettsiales" total_count="19">
                    <taxon self_count="0" tax_id="255531" name="Rickettsiales genera incertae sedis" total_count="1">
                      <taxon self_count="1" tax_id="28905" rank="genus" name="Caedibacter" total_count="1"/>
                    </taxon>
                    <taxon self_count="5" tax_id="942" rank="family" name="Anaplasmataceae" total_count="18">
                      <taxon self_count="0" tax_id="952" rank="tribe" name="Wolbachieae" total_count="13">
                        <taxon self_count="13" tax_id="953" rank="genus" name="Wolbachia" total_count="13"/>
                      </taxon>
                    </taxon>
                  </taxon>
                  <taxon self_count="7" tax_id="204457" rank="order" name="Sphingomonadales" total_count="105">
                    <taxon self_count="38" tax_id="41297" rank="family" name="Sphingomonadaceae" total_count="98">
                      <taxon self_count="29" tax_id="13687" rank="genus" name="Sphingomonas" total_count="29"/>
                      <taxon self_count="0" tax_id="165695" rank="genus" name="Sphingobium" total_count="31">
                        <taxon self_count="31" tax_id="13690" rank="species" name="Sphingobium yanoikuyae" total_count="31"/>
                      </taxon>
                    </taxon>
                  </taxon>
                  <taxon self_count="0" tax_id="204458" rank="order" name="Caulobacterales" total_count="36">
                    <taxon self_count="0" tax_id="76892" rank="family" name="Caulobacteraceae" total_count="36">
                      <taxon self_count="0" tax_id="75" rank="genus" name="Caulobacter" total_count="6">
                        <taxon self_count="6" tax_id="69395" rank="species" name="Caulobacter henricii" total_count="6"/>
                      </taxon>
                      <taxon self_count="0" tax_id="20" rank="genus" name="Phenylobacterium" total_count="12">
                        <taxon self_count="0" tax_id="284016" rank="species" name="Phenylobacterium zucineum" total_count="12">
                          <taxon self_count="12" tax_id="450851" name="Phenylobacterium zucineum HLK1" total_count="12"/>
                        </taxon>
                      </taxon>
                      <taxon self_count="0" tax_id="41275" rank="genus" name="Brevundimonas" total_count="18">
                        <taxon self_count="18" tax_id="293" rank="species" name="Brevundimonas diminuta" total_count="18"/>
                      </taxon>
                    </taxon>
                  </taxon>
                  <taxon self_count="0" tax_id="356" rank="order" name="Rhizobiales" total_count="205">
                    <taxon self_count="0" tax_id="82115" rank="family" name="Rhizobiaceae" total_count="144">
                      <taxon self_count="139" tax_id="227290" name="Rhizobium/Agrobacterium group" total_count="144">
                        <taxon self_count="3" tax_id="357" rank="genus" name="Agrobacterium" total_count="3"/>
                        <taxon self_count="0" tax_id="379" rank="genus" name="Rhizobium" total_count="2">
                          <taxon self_count="2" tax_id="424182" rank="species" name="Rhizobium sp. IRBG74" total_count="2"/>
                        </taxon>
                      </taxon>
                    </taxon>
                    <taxon self_count="0" tax_id="255475" rank="family" name="Aurantimonadaceae" total_count="2">
                      <taxon self_count="0" tax_id="414371" rank="genus" name="Aureimonas" total_count="2">
                        <taxon self_count="2" tax_id="370622" rank="species" name="Aureimonas altamirensis" total_count="2"/>
                      </taxon>
                    </taxon>
                    <taxon self_count="0" tax_id="119045" rank="family" name="Methylobacteriaceae" total_count="59">
                      <taxon self_count="59" tax_id="407" rank="genus" name="Methylobacterium" total_count="59"/>
                    </taxon>
                  </taxon>
                  <taxon self_count="0" tax_id="82117" name="unclassified Alphaproteobacteria" total_count="22">
                    <taxon self_count="0" tax_id="33807" name="unclassified Alphaproteobacteria (miscellaneous)" total_count="22">
                      <taxon self_count="22" tax_id="1229204" rank="species" name="alpha proteobacterium L41A" total_count="22"/>
                    </taxon>
                  </taxon>
                </taxon>
                <taxon self_count="0" tax_id="68525" rank="subphylum" name="delta/epsilon subdivisions" total_count="2">
                  <taxon self_count="0" tax_id="29547" rank="class" name="Epsilonproteobacteria" total_count="2">
                    <taxon self_count="0" tax_id="213849" rank="order" name="Campylobacterales" total_count="2">
                      <taxon self_count="0" tax_id="72294" rank="family" name="Campylobacteraceae" total_count="2">
                        <taxon self_count="0" tax_id="194" rank="genus" name="Campylobacter" total_count="2">
                          <taxon self_count="2" tax_id="827" rank="species" name="Campylobacter ureolyticus" total_count="2"/>
                        </taxon>
                      </taxon>
                    </taxon>
                  </taxon>
                </taxon>
              </taxon>
              <taxon self_count="0" tax_id="1783270" name="FCB group" total_count="214">
                <taxon self_count="0" tax_id="68336" name="Bacteroidetes/Chlorobi group" total_count="214">
                  <taxon self_count="9" tax_id="976" rank="phylum" name="Bacteroidetes" total_count="214">
                    <taxon self_count="0" tax_id="117743" rank="class" name="Flavobacteriia" total_count="184">
                      <taxon self_count="0" tax_id="200644" rank="order" name="Flavobacteriales" total_count="184">
                        <taxon self_count="43" tax_id="49546" rank="family" name="Flavobacteriaceae" total_count="184">
                          <taxon self_count="0" tax_id="308865" rank="genus" name="Elizabethkingia" total_count="8">
                            <taxon self_count="2" tax_id="722877" rank="species" name="Elizabethkingia miricola" total_count="2"/>
                            <taxon self_count="6" tax_id="1117645" rank="species" name="Elizabethkingia anophelis" total_count="6"/>
                          </taxon>
                          <taxon self_count="0" tax_id="59734" rank="genus" name="Empedobacter" total_count="15">
                            <taxon self_count="15" tax_id="343874" rank="species" name="Empedobacter falsenii" total_count="15"/>
                          </taxon>
                          <taxon self_count="117" tax_id="59732" rank="genus" name="Chryseobacterium" total_count="118">
                            <taxon self_count="0" tax_id="365343" rank="species" name="Chryseobacterium caeni" total_count="1">
                              <taxon self_count="1" tax_id="1121285" name="Chryseobacterium caeni DSM 17710" total_count="1"/>
                            </taxon>
                          </taxon>
                        </taxon>
                      </taxon>
                    </taxon>
                    <taxon self_count="0" tax_id="200643" rank="class" name="Bacteroidia" total_count="20">
                      <taxon self_count="0" tax_id="171549" rank="order" name="Bacteroidales" total_count="20">
                        <taxon self_count="20" tax_id="171551" rank="family" name="Porphyromonadaceae" total_count="20"/>
                      </taxon>
                    </taxon>
                    <taxon self_count="0" tax_id="768503" rank="class" name="Cytophagia" total_count="1">
                      <taxon self_count="1" tax_id="768507" rank="order" name="Cytophagales" total_count="1"/>
                    </taxon>
                  </taxon>
                </taxon>
              </taxon>
              <taxon self_count="0" tax_id="32066" rank="phylum" name="Fusobacteria" total_count="23">
                <taxon self_count="0" tax_id="203490" rank="class" name="Fusobacteriia" total_count="23">
                  <taxon self_count="0" tax_id="203491" rank="order" name="Fusobacteriales" total_count="23">
                    <taxon self_count="0" tax_id="203492" rank="family" name="Fusobacteriaceae" total_count="18">
                      <taxon self_count="18" tax_id="848" rank="genus" name="Fusobacterium" total_count="18"/>
                    </taxon>
                    <taxon self_count="0" tax_id="1129771" rank="family" name="Leptotrichiaceae" total_count="5">
                      <taxon self_count="0" tax_id="32067" rank="genus" name="Leptotrichia" total_count="5">
                        <taxon self_count="0" tax_id="157691" rank="species" name="Leptotrichia shahii" total_count="5">
                          <taxon self_count="5" tax_id="1122172" name="Leptotrichia shahii DSM 19757" total_count="5"/>
                        </taxon>
                      </taxon>
                    </taxon>
                  </taxon>
                </taxon>
              </taxon>
              <taxon self_count="0" tax_id="1853220" rank="phylum" name="Rhodothermaeota" total_count="3">
                <taxon self_count="0" tax_id="1853221" rank="class" name="Balneolia" total_count="3">
                  <taxon self_count="0" tax_id="1853223" rank="order" name="Balneolales" total_count="3">
                    <taxon self_count="0" tax_id="1813606" rank="family" name="Balneolaceae" total_count="3">
                      <taxon self_count="0" tax_id="455358" rank="genus" name="Balneola" total_count="3">
                        <taxon self_count="0" tax_id="287535" rank="species" name="Balneola vulgaris" total_count="3">
                          <taxon self_count="3" tax_id="1121104" name="Balneola vulgaris DSM 17893" total_count="3"/>
                        </taxon>
                      </taxon>
                    </taxon>
                  </taxon>
                </taxon>
              </taxon>
            </taxon>
          </taxon>
          <taxon self_count="0" tax_id="10239" rank="superkingdom" name="Viruses" total_count="70">
            <taxon self_count="0" tax_id="35237" name="dsDNA viruses, no RNA stage" total_count="61">
              <taxon self_count="0" tax_id="28883" rank="order" name="Caudovirales" total_count="12">
                <taxon self_count="0" tax_id="10744" rank="family" name="Podoviridae" total_count="3">
                  <taxon self_count="0" tax_id="542835" rank="subfamily" name="Autographivirinae" total_count="3">
                    <taxon self_count="0" tax_id="110456" rank="genus" name="T7likevirus" total_count="2">
                      <taxon self_count="0" tax_id="329157" name="unclassified T7-like viruses" total_count="2">
                        <taxon self_count="2" tax_id="10759" rank="species" name="Enterobacteria phage T3" total_count="2"/>
                      </taxon>
                    </taxon>
                    <taxon self_count="0" tax_id="477967" rank="genus" name="Phikmvlikevirus" total_count="1">
                      <taxon self_count="1" tax_id="386793" rank="species" name="Pseudomonas phage LKA1" total_count="1"/>
                    </taxon>
                  </taxon>
                </taxon>
                <taxon self_count="4" tax_id="10699" rank="family" name="Siphoviridae" total_count="9">
                  <taxon self_count="2" tax_id="196894" name="unclassified Siphoviridae" total_count="5">
                    <taxon self_count="0" tax_id="1647434" rank="species" name="Propionibacterium phage PHL150" total_count="3">
                      <taxon self_count="3" tax_id="1500822" name="Propionibacterium phage PHL150M00" total_count="3"/>
                    </taxon>
                  </taxon>
                </taxon>
              </taxon>
              <taxon self_count="0" tax_id="10442" rank="family" name="Baculoviridae" total_count="49">
                <taxon self_count="26" tax_id="558016" rank="genus" name="Alphabaculovirus" total_count="49">
                  <taxon self_count="0" tax_id="307456" rank="species" name="Autographa californica multiple nucleopolyhedrovirus" total_count="23">
                    <taxon self_count="23" tax_id="46015" name="Autographa californica nucleopolyhedrovirus" total_count="23"/>
                  </taxon>
                </taxon>
              </taxon>
            </taxon>
            <taxon self_count="0" tax_id="439488" name="ssRNA viruses" total_count="9">
              <taxon self_count="0" tax_id="35278" name="ssRNA positive-strand viruses, no DNA stage" total_count="9">
                <taxon self_count="0" tax_id="464095" rank="order" name="Picornavirales" total_count="3">
                  <taxon self_count="0" tax_id="232795" rank="family" name="Dicistroviridae" total_count="3">
                    <taxon self_count="0" tax_id="144051" rank="genus" name="Cripavirus" total_count="3">
                      <taxon self_count="3" tax_id="64279" rank="species" name="Drosophila C virus" total_count="3"/>
                    </taxon>
                  </taxon>
                </taxon>
                <taxon self_count="0" tax_id="12283" rank="family" name="Nodaviridae" total_count="6">
                  <taxon self_count="0" tax_id="143920" rank="genus" name="Alphanodavirus" total_count="6">
                    <taxon self_count="6" tax_id="12287" rank="species" name="Flock house virus" total_count="6"/>
                  </taxon>
                </taxon>
              </taxon>
            </taxon>
          </taxon>
        </tax_analysis>
      </RUN>
    </RUN_SET>
    """




EXISTING_STUDY_TYPES_ACTIVE = [
    "Whole Genome Sequencing",
    "Metagenomics",
    "Transcriptome Analysis",
    "Epigenetics",
    "Synthetic Genomics",
    "Cancer Genomics",
    "Population Genomics",
    "Exome Sequencing",
    "Pooled Clone Sequencing",
    "Other"
    ]

EXISTING_STUDY_TYPES_DEPRICATED = {
    "Resequencing": "Whole Genome Sequencing",
    "Forensic or Paleo-genomics": "Other",
    "Gene Regulation Study": "Transcriptome Analysis",
    "RNASeq": "Transcriptome Sequencing"
    }


PLATFORM_TYPE_ACTIVE = {
    "LS454": [
        "454 GS",
        "454 GS 20",
        "454 GS FLX",
        "454 GS FLX+",
        "454 GS FLX Titanium",
        "454 GS Junior",
        "unspecified",
        ],
    "ILLUMINA": [
        "Illumina Genome Analyzer",
        "Illumina Genome Analyzer II",
        "Illumina Genome Analyzer IIx",
        "Illumina HiSeq 2500",
        "Illumina HiSeq 2000",
        "Illumina HiSeq 1000",
        "Illumina MiSeq",
        "Illumina HiScanSQ",
        "unspecified",
        ],
    "HELICOS": [
        "Helicos HeliScope",
        "unspecified",
        ],
    "ABI_SOLID": [
        "AB SOLiD System",
        "AB SOLiD System 2.0",
        "AB SOLiD System 3.0",
        "AB SOLiD 3 Plus System",
        "AB SOLiD 4 System",
        "AB SOLiD 4hq System",
        "AB SOLiD PI System",
        "AB 5500 Genetic Analyzer",
        "AB 5500xl Genetic Analyzer",
        "unspecified",
        ],
    "COMPLETE_GENOMICS": [
        "Complete Genomics",
        "unspecified",
        ],
    "PACBIO_SMRT": [
        "PacBio RS",
        "unspecified",
        ],
    "ION_TORRENT": [
        "Ion Torrent PGM",
        "Ion Torrent Proton",
        "unspecified",
        ],
    "CAPILLARY": [
        "AB 3730xL Genetic Analyzer",
        "AB 3730 Genetic Analyzer",
        "AB 3500xL Genetic Analyzer",
        "AB 3500 Genetic Analyzer",
        "AB 3130xL Genetic Analyzer",
        "AB 3130 Genetic Analyzer",
        "AB 310 Genetic Analyzer",
        "unspecified",
        ],

    }

PLATFORM_TYPE_DEPRICATED = {
    "AB SOLiD 5500": "AB 5500 Genetic Analyzer",
    "AB SOLiD 5500xl": "AB 5500xl Genetic Analyzer",
    }

if __name__ == '__main__':
    pass