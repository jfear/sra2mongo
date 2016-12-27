"""Constants from SRA XML schema."""

EXISTING_STUDY_TYPES_ACTIVE = [
    "Cancer Genomics",
    "Epigenetics",
    "Exome Sequencing",
    "Metagenomics",
    "Other"
    "Pooled Clone Sequencing",
    "Population Genomics",
    "Synthetic Genomics",
    "Transcriptome Analysis",
    "Whole Genome Sequencing",
    ]

EXISTING_STUDY_TYPES_DEPRICATED = {
    "Resequencing": "Whole Genome Sequencing",
    "Forensic or Paleo-genomics": "Other",
    "Gene Regulation Study": "Transcriptome Analysis",
    "RNASeq": "Transcriptome Sequencing"
    }

LIBRARY_STRATEGY = [
    "AMPLICON",
    "Bisulfite-Seq",
    "ChIP-Seq",
    "CLONE",
    "CLONEEND",
    "CTS",
    "DNase-Hypersensitivity",
    "EST",
    "FINISHING",
    "FL-cDNA",
    "MBD-Seq",
    "MeDIP-Seq",
    "miRNA-Seq",
    "MNase-Seq",
    "MRE-Seq",
    "OTHER",
    "POOLCLONE",
    "RNA-Seq",
    "Tn-Seq",
    "WCS",
    "WGA",
    "WGS",
    "WXS",
    ]

LIBRARY_SOURCE = [
    "GENOMIC",
    "METAGENOMIC",
    "METATRANSCRIPTOMIC",
    "NON GENOMIC",
    "OTHER",
    "SYNTHETIC",
    "TRANSCRIPTOMIC",
    "VIRAL RNA",
    ]

LIBRARY_SELECTION = [
    "5-methylcytidine antibody",
    "CAGE",
    "cDNA",
    "CF-H",
    "CF-M",
    "CF-S",
    "CF-T",
    "ChIP",
    "DNAse",
    "HMPR",
    "Hybrid Selection",
    "MBD2 protein methyl-CpG binding domain",
    "MDA",
    "MF",
    "MNase",
    "MSLL",
    "other",
    "padlock probes capture method",
    "PCR",
    "RACE",
    "RANDOM",
    "RANDOM PCR",
    "Reduced Representation",
    "Restriction Digest",
    "RT-PCR",
    "size fractionation",
    "unspecified",
    ]

LIBRARY_LAYOUT = [
    "PAIRED",
    "SINGLE",
    ]

PLATFORMS = [
    "ABI_SOLID",
    "CAPILLARY",
    "COMPLETE_GENOMICS",
    "HELICOS",
    "ILLUMINA",
    "ION_TORRENT",
    "LS454",
    "PACBIO_SMRT",
    ]

INSTRUMENT_MODEL_ACTIVE = [
    "454 GS",
    "454 GS 20",
    "454 GS FLX",
    "454 GS FLX+",
    "454 GS FLX Titanium",
    "454 GS Junior",
    "AB 310 Genetic Analyzer",
    "AB 3130 Genetic Analyzer",
    "AB 3130xL Genetic Analyzer",
    "AB 3500 Genetic Analyzer",
    "AB 3500xL Genetic Analyzer",
    "AB 3730 Genetic Analyzer",
    "AB 3730xL Genetic Analyzer",
    "AB 5500 Genetic Analyzer",
    "AB 5500xl Genetic Analyzer",
    "AB SOLiD 3 Plus System",
    "AB SOLiD 4hq System",
    "AB SOLiD 4 System",
    "AB SOLiD PI System",
    "AB SOLiD System",
    "AB SOLiD System 2.0",
    "AB SOLiD System 3.0",
    "Complete Genomics",
    "Helicos HeliScope",
    "Illumina Genome Analyzer",
    "Illumina Genome Analyzer II",
    "Illumina Genome Analyzer IIx",
    "Illumina HiScanSQ",
    "Illumina HiSeq 1000",
    "Illumina HiSeq 2000",
    "Illumina HiSeq 2500",
    "Illumina MiSeq",
    "Ion Torrent PGM",
    "Ion Torrent Proton",
    "PacBio RS",
    "unspecified",
    ]

INSTRUMENT_MODEL_DEPRICATED = {
    "AB SOLiD 5500": "AB 5500 Genetic Analyzer",
    "AB SOLiD 5500xl": "AB 5500xl Genetic Analyzer",
    }
