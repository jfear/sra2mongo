"""Parse parts of the SRA XML into JSON."""
from typing import Union, IO
from xml.etree import cElementTree as ElementTree

from .models import SraDocument, Study, Organization, Sample, Run


def xml_to_root(xml: Union[str, IO]) -> ElementTree.Element:
    """Parse XML into an ElemeTree object.

    Parameters
    ----------
    xml : str or file-like object
        A filename, file object or string version of xml can be passed.

    Returns
    -------
    Elementree.Element

    """
    if isinstance(xml, str):
        if '<' in xml:
            return ElementTree.fromstring(xml)
        else:
            with open(xml) as fh:
                xml_to_root(fh)
    tree = ElementTree.parse(xml)
    return tree.getroot()


def parse_sra_experiment(root):
    sra = SraDocument()

    # Experiment information
    sra.accn = get_xml_text(root, 'EXPERIMENT/IDENTIFIERS/PRIMARY_ID')
    sra.title = get_xml_text(root, 'EXPERIMENT/TITLE')
    sra.design = get_xml_text(root, 'EXPERIMENT/DESIGN/DESIGN_DESCRIPTION')
    sra.library_name = get_xml_text(root, 'EXPERIMENT/DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_NAME')
    sra.library_strategy = get_xml_text(root, 'EXPERIMENT/DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_STRATEGY')
    sra.library_source = get_xml_text(root, 'EXPERIMENT/DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_SOURCE')
    sra.library_selection = get_xml_text(root, 'EXPERIMENT/DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_SELECTION')
    sra.library_construction_protocol = get_xml_text(root, 'EXPERIMENT/DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_CONSTRUCTION_PROTOCOL')
    add_library_layout(root, sra)
    add_platform_information(root, sra)

    # Embeded Documents
    sra.study = parse_sra_study(root)
    sra.organization = parse_sra_organization(root)
    sra.sample = parse_sra_sample(root)
    sra.run = parse_sra_run(root)


def parse_sra_study(root):
    study = Study()
    study.accn = get_xml_text(root, 'STUDY/IDENTIFIERS/PRIMARY_ID')
    study.title = get_xml_text(root, 'STUDY/DESCRIPTOR/STUDY_TITLE')
    study.abstract = get_xml_text(root, 'STUDY/DESCRIPTOR/STUDY_ABSTRACT')
    study.center_name = get_xml_attribute(root, 'STUDY', 'center_name')
    study.center_project_name = get_xml_text(root, 'STUDY/DESCRIPTOR/CENTER_PROJECT_NAME')

    description = get_xml_text(root, 'STUDY/DESCRIPTOR/STUDY_DESCRIPTION')
    if description is not None and description != study.abstract:
        study.description = get_xml_text(root, '')
    return study


def parse_sra_organization(root):
    organization = Organization()
    organization.organization_type = get_xml_attribute(root, 'Organization', 'type')
    organization.abbreviation = get_xml_attribute(root, 'Organization/Name', 'abbr')
    organization.name = get_xml_text(root, 'Organization/Name')
    organization.email = get_xml_attribute(root, 'Organization/Contact', 'email')
    organization.first_name = get_xml_text(root, 'Organization/Contact/NAME/FIRST')
    organization.last_name = get_xml_text(root, 'Organization/Contact/NAME/FIRST')
    return organization


def parse_sra_sample(root):
    sample = Sample()
    sample.accn = get_xml_text(root, 'SAMPLE/IDENTIFIERS/PRIMARY_ID')
    sample.title = get_xml_text(root, 'SAMPLE/TITLE')
    sample.taxon_id = get_xml_text(root, 'SAMPLE/SAMPLE_NAME/TAXON_ID')
    sample.scientific_name = get_xml_text(root, 'SAMPLE/SAMPLE_NAME/SCIENTIFIC_NAME')
    sample.common_name = get_xml_text(root, 'SAMPLE/SAMPLE_NAME/COMMON_NAME')
    add_sample_attributes(root, sample)
    return sample


def parse_sra_run(root):
    runs = []
    for run in root.findall('RUN_SET/RUN'):
        sra_run = Run()
        run.accn = get_xml_text(root, 'RUN/IDENTIFIERS/PRIMARY_ID')
        run.nspots = int(get_xml_attribute(run, 'RUN', 'total_spots'))
        run.nbases = int(get_xml_attribute(run, 'RUN', 'total_bases'))
        run.nreads = int(get_xml_attribute(run, 'RUN/Bases', 'count'))

        # # if single ended then just use _r1
        # read_count_r1 = FloatField()
        # read_len_r1 = FloatField()
        #
        # read_count_r2 = FloatField()
        # read_len_r2 = FloatField()
        #
        # # NOTE: Additional Fields not in the SRA XML but in summary table
        # release_date = DateTimeField()
        # load_date = DateTimeField()
        # size_MB = IntField()
        runs.append(sra_run)

    return runs


def get_xml_text(root, path):
    try:
        return root.find(path).text
    except:
        return ''


def get_xml_attribute(root, path, attribute):
    try:
        return root.find(path).attrib[attribute]
    except:
        return ''


def add_library_layout(root, sra):
    if root.find('EXPERIMENT/DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_LAYOUT/SINGLE') is not None:
        sra.library_layout = 'SINGLE'
    else:
        sra.library_layout = 'PARIED'
        sra.library_layout_length = int(get_xml_attribute(root, 'EXPERIMENT/DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_LAYOUT/PAIRED', 'NOMINAL_LENGTH'))
        sra.library_layout_sdev = float(get_xml_attribute(root, 'EXPERIMENT/DESIGN/LIBRARY_DESCRIPTOR/LIBRARY_LAYOUT/PAIRED', 'NOMINAL_SDEV'))
    return sra


def add_platform_information(root, sra):
    sra.platform = root.find('EXPERIMENT/PLATFORM').getchildren()[0].tag
    sra.instrument_model = get_xml_text(root, f'EXPERIMENT/PLATFORM/{sra.platform}/INSTRUMENT_MODEL')
    return sra


def add_sample_attributes(root, sample):
    for attribute in root.findall('SAMPLE/SAMPLE_ATTRIBUTES/SAMPLE_ATTRIBUTE'):
        tag = attribute.find('TAG').text
        value = attribute.find('VALUE').text
        sample.attributes.append({'name': tag, 'value': value})

