
import os
import tempfile
import pandas as pd
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
import gzip
import argparse
from ancient_helper_kit.util.general import download_via_http_link, is_gz_file, create_stdout_logger
import sys
from multiprocessing import Process, Queue
from typing import Set, Dict

taxonomy_acc2taxId = "https://ftp.ncbi.nih.gov/pub/taxonomy/accession2taxid/nucl_gb.accession2taxid.gz"
genbank_and_refseq_nucleotide_sequences = "http://ftp.ncbi.nlm.nih.gov/genomes/Viruses/AllNucleotide/AllNucleotide.fa"
genbank_and_refseq_nucleotide_meta_data = "https://ftp.ncbi.nlm.nih.gov/genomes/Viruses/AllNuclMetadata/AllNuclMetadata.csv"

meta_data_dtypes = {"#Accession": str,
                     "SRA_Accession": str,
                     "Submitters": str,
                     "Release_Date": str,
                     "Species": str,
                     "Genus": str,
                     "Family": str,
                     "Molecule_type": str,
                     "Length": int,
                     "Sequence_Type": str,
                     "Nuc_Completeness": str,
                    "Genotype": str,
                    "Segment": str,
                    "Publications": float,
                    "Geo_Location": str,
                    "USA": str,
                    "Host": str,
                    "Isolation_Source": str,
                    "Collection_Date": str,
                    "BioSample": str,
                    "GenBank_Title": str,
                    "phage": bool}


def handle_meta_data(in_fn):
    """
    Filter the meta data file down to DNA viruses and try to exclude phages.
    @param in_fn: csv file from NCBI giving meta info about the viral genome sequences from refseq/genbank
    @return: dataframe containing the csv file filtered down
    """
    df_meta = pd.read_csv(in_fn, dtype=meta_data_dtypes)

    def is_phage(row):
        return (("phage" in str(row.Species).lower())
                or "bacteria" in str(row.Host).lower()
                or "bacterium" in str(row.Host).lower()
                or "phage" in str(row.GenBank_Title).lower()
                or "bacterium" in str(row.GenBank_Title).lower())

    df_meta['is_phage'] = df_meta.apply(is_phage, axis=1)
    df_meta['is_dna_virus'] = df_meta.Molecule_type.apply(lambda x: "dna" in str(x).lower())

    df_complete = df_meta[(df_meta.Nuc_Completeness == 'complete')
                          & (~df_meta.is_phage)
                          & df_meta.is_dna_virus]
    return df_complete


def filter_nuc_sequences(nuc_fn: str, filter_set: Set[str], queue=None) -> Dict[str, SeqRecord]:
    """
    Filters out FASTA records from a FASTA file whose Ids are not in the given set and
    returns the records in a dict[str, SeqRecord] with the fasta id as key.
    :param nuc_fn: file name of the fasta file
    :param filter_set: set with allowed ids (whitelist)
    :param queue: necessary if called within a separate process to return the dict
    :return: dict[str, SeqRecord] with the fasta id as key
    """
    ncbi_dict = dict()
    for record in SeqIO.parse(open(nuc_fn), 'fasta'):
        accession = record.id.split('|')[0]
        if accession in filter_set:
            ncbi_dict[accession] = record
    queue.put(('seq_dic', ncbi_dict)) if queue else None
    return ncbi_dict


def read_in_acc_to_taxid(in_fn, filter_set=None, queue=None):
    """
    Iterates over the content of the accession2taxid file that links
    accession ids to tax ids and returns a dictionary with accession:[taxId]
    If filter_set is given only accessions that are in the set are returned.
    @param in_fn:
    @param filter_set:
    @param queue: needs to be specified if run in a separate process to be able to return sth
    @return:
    """
    rd = dict()
    f = gzip.open(in_fn, 'rt') if is_gz_file(in_fn) else open(in_fn)
    with f as fp:
        # accession accession.version   taxid   gi
        fp.readline()  # skip header
        for line in fp:
            _, accession, tax_id, _ = line.strip().split('\t')
            if filter_set:
                if accession in filter_set:
                    assert accession not in rd, f"accession {accession} occurred twice in input file"
                    rd[accession] = tax_id
            else:
                assert accession not in rd, f"accession {accession} occurred twice in input file"
                rd[accession] = tax_id
    queue.put(('tax_id', rd)) if queue is not None else None
    return rd


def my_generator(seq_dict, tax_lookup, meta_df=None):
    """
    Generator taking a dictionary of fasta sequences and a dictionary with accession number
    as key and tax id as value.
    The generator iterates over the dictionary content, if the accession number of the sequence
    is in the tax_lookup dictionary it will add a kraken-specific signature to the fasta description
    that includes the tax-id and yield that modified fasta entry.
    @param seq_dict: dictionary containing fasta sequences {accession: SeqRecord}
    @param tax_lookup: dictionary containing tax-ids entries {accession: tax-id}
    @param meta_df: dataframe with meta information of the sequence
    @return: yields fasta-records with a kraken-specific description
    """
    for k, record in seq_dict.items():
        if k in tax_lookup:
            tax_id = tax_lookup[k]
            new_name = f"{k}|kraken:taxid|{tax_id}"
            if meta_df is not None:
                df = meta_df[meta_df["#Accession"] == k]
                assert len(df) == 1, f"meta_df contains more than one entry or none for accession: {record.id}"
                new_description = f"{new_name} {df.GenBank_Title.values[0]}"
            else:
                # extracting the description only without the id
                t = record.description.split(" ", maxsplit=1)
                new_description = new_name if len(t) == 1 else f"{new_name} {t[-1]}"
            yield SeqRecord(record.seq, id=record.id, name=new_name, description=new_description)


def parse_meta_data(args, my_logger):
    """
    Either downloads or gets metadata about the corresponding fasta file.
    Then it filters down to my chosen criteria.
    :param args: args from the argparser
    :param my_logger: reference to a logger
    :return: filtered data frame of the meta data
    """
    if args.meta:
        my_logger.info('meta data provided, reading and filtering it next ...')
        meta_df = handle_meta_data(args.meta)
    else:
        my_logger.info('meta data not provided, downloading it next ...')
        fp = tempfile.NamedTemporaryFile(delete=False)
        download_via_http_link(genbank_and_refseq_nucleotide_meta_data, out_fn=fp.name)
        my_logger.info('downloading done, next filtering....')
        meta_df = handle_meta_data(fp.name)
        fp.close()
        os.remove(fp.name)
    my_logger.info('finished handling of meta data')
    if args.out_fn_meta:
        my_logger.info(f"writing out meta data to: {args.out_fn_meta}")
        meta_df.to_csv(args.out_fn_meta, index=False)
    return meta_df


def filter_tax_id_mapping(args, my_logger, my_queue, sub_set, temp_file_list):
    # tax id mapping
    if args.acc2tax:
        p1 = Process(target=read_in_acc_to_taxid, args=(args.acc2tax,), kwargs={"filter_set": sub_set,
                                                                                "queue": my_queue})
        p1.start()
        my_logger.info("starting the acc2tax parsing ...")
    else:
        fp_acc2tax = tempfile.NamedTemporaryFile(delete=False)
        temp_file_list.append(fp_acc2tax)
        my_logger.info("downloading the acc2tax id mappings ...")
        p1 = Process(target=download_via_http_link, args=(taxonomy_acc2taxId,), kwargs={'out_fn': fp_acc2tax.name})
        p1.start(), p1.join()

        p1 = Process(target=read_in_acc_to_taxid, args=(fp_acc2tax.name,), kwargs={"filter_set": sub_set,
                                                                                   "queue": my_queue})
        p1.start()
        my_logger.info("starting the acc2tax parsing ...")
    return p1


def handle_nucleotide_fasta(args, my_logger, my_queue, sub_set, temp_file_list):
    # nucs
    if args.nuc:
        p2 = Process(target=filter_nuc_sequences, args=(args.nuc, sub_set), kwargs={"queue": my_queue})
        p2.start()
        my_logger.info("starting to parse the nuc sequences ...")
    else:
        fp_nucs = tempfile.NamedTemporaryFile(delete=False)
        temp_file_list.append(fp_nucs)
        p2 = Process(target=download_via_http_link, args=(genbank_and_refseq_nucleotide_sequences,),
                     kwargs={'out_fn': fp_nucs.name})
        p2.start(), p2.join()

        p2 = Process(target=filter_nuc_sequences, args=(fp_nucs.name, sub_set), kwargs={"queue": my_queue})
        p2.start()
    return p2


def create_arg_parser(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('out_fn', help='output file name for the FASTA file')
    parser.add_argument("--meta", help='file with ncbi meta data')
    parser.add_argument("--nuc", help='file with ncbi sequence records as FASTA')
    parser.add_argument("--acc2tax", help='file with accession2taxid mapping')
    parser.add_argument("--out_fn_meta", help="output the filtered meta data to this file")
    args = parser.parse_args(argv)
    return args


def main(argv):
    args = create_arg_parser(argv)
    my_logger = create_stdout_logger()

    # meta data
    meta_df = parse_meta_data(args, my_logger)
    sub_set = set(meta_df["#Accession"])

    # tax id and nucs
    my_queue = Queue()
    temp_file_list = list()  # needed as only after the spawned processes are done i can delete these files

    p1 = filter_tax_id_mapping(args, my_logger, my_queue, sub_set, temp_file_list)
    p2 = handle_nucleotide_fasta(args, my_logger, my_queue, sub_set, temp_file_list)

    qe1, qe2 = my_queue.get(), my_queue.get()
    p1.join(), p2.join()
    [(fp.close(), os.remove(fp.name)) for fp in temp_file_list]

    my_logger.info('done with parsing both, writing out the result next')
    # figure out who came out the queue first
    if qe1[0] == 'seq_dict':
        seq_dict, tax_dic = qe1[1], qe2[1]
    else:
        seq_dict, tax_dic = qe2[1], qe1[1]

    with open(args.out_fn, 'w') as handle:
        SeqIO.write(my_generator(seq_dict, tax_dic, meta_df), handle, "fasta")
    my_logger.info('done with everything')


if __name__ == "__main__":
    main(sys.argv[1:])
