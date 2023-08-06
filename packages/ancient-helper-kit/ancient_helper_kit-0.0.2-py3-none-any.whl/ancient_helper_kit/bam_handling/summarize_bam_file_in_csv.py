import pysam
import pandas as pd
import numpy as np
from collections import defaultdict
from math import ceil
from Bio import SeqIO
import sys
import logging
from ancient_helper_kit.util.general import create_stdout_logger

def get_buckets(arr):

    # to make this comparable, compute the percentage of reads
    # in each of 100 buckets of the genome, so you can say 10% of the reads are in the first 2% of the genome
    step_size = int(ceil(len(arr) / 100))
    res = np.zeros(100)

    generator = (slice(i, min(i + step_size, len(arr))) for i in range(0, len(arr), step_size))
    for i, sl in enumerate(generator):
        res[i] = arr[sl].sum() / arr.sum()
    return ','.join(res.astype(str))


def standardize(arr):
    return (arr-arr.mean())/arr.std()


def sample_coverage_and_call_agg_functions(dic, row, agg_funcs, no_samples=50, sample_ratio=0.66):
    """
    Given a row of the dataframe, that represents a virus-accession, this function looks up the found
    alignment from the bam file via the passed dictionary.
    It then creates a vector representing the coverage found for the respective full virus genome.
    From this vector samples are taken multiple times. The provided functions are then applied on these
    samples. These functions should compute aggregations of the coverage samples, like the mean/median/std.
    @param dic: dictionary with key: NC accession value: pysam alignment
    @param row: a row from the dataframe, containing information about the length and nc accesion of the virus
    @param agg_funcs: function that takes as input a 2D numpy array
    @param no_samples: the number of samples that should be drawn
    @param sample_ratio: the number of locations across the genome that should be assembled, specified as ratio of
    the full genome length
    @return: list with output of the passed functions
    """
    if len(dic[row.name]) == 0:  # not a single alignment found
        return [0 for f in agg_funcs]

    virus_length = row.length
    # create an array to compute the coverage at each position
    coverage_arr = np.zeros(virus_length)
    for m in dic[row.name]:
        coverage_arr[m.get_reference_positions()] += 1

    standardized_cov_arr = standardize(coverage_arr)

    # considering everything above of x times the standard deviation as an outlier
    cleaned5 = standardized_cov_arr[standardized_cov_arr < 5]
    cleaned3 = standardized_cov_arr[standardized_cov_arr < 3]
    cleaned7 = standardized_cov_arr[standardized_cov_arr < 7]

    res = [f(cleaned3) for f in agg_funcs]
    res += [f(cleaned5) for f in agg_funcs]
    res += [f(cleaned7) for f in agg_funcs]
    res.append(get_buckets(coverage_arr))
    res.append((coverage_arr >= 1).sum()/virus_length)
    return res


if __name__ == '__main__':

    with open(snakemake.log.stderr, 'w') as fp_stderr:
        with open(snakemake.log.stdout, 'w') as fp_stdout:
            sys.stderr = fp_stderr
            sys.stdout = fp_stdout
            my_logger = create_stdout_logger()
            my_logger.info('start to read in alignment')
            alignment_lookup = defaultdict(list)
            for alignment in pysam.AlignmentFile(snakemake.input.bam, "rb"):
                alignment_lookup[alignment.reference_name].append(alignment)
            my_logger.info('done')
            if len(alignment_lookup) > 0:
                fasta_sequences = SeqIO.parse(open(snakemake.input.virus_fasta),'fasta')
                temp_list = [[fasta.id, fasta.description, len(fasta.seq)] for fasta in fasta_sequences]

                df1 = pd.DataFrame(temp_list, columns=['nc_accession', 'description', 'length'])
                df2 = pd.DataFrame([[k, len(v)] for (k,v) in alignment_lookup.items()], columns=['nc_accession', 'no_mappings'])
                df = df1.merge(df2, left_on="nc_accession", right_on="nc_accession")
                df.set_index('nc_accession', inplace=True)
                my_logger.info('merging done')

                agg_funcs = [('std', np.std),
                             ('mean', np.mean),
                             ('95_perc', lambda x: np.quantile(x,.95)),
                             ]
                new_cols = [f"{name}_{n}" for n in ["3", "5","7"] for name, _ in agg_funcs ]
                new_cols.append('read_coverage_buckets')
                new_cols.append('breadth')
                df[new_cols] = df.apply(lambda row: sample_coverage_and_call_agg_functions(
                    dic=alignment_lookup, row=row, agg_funcs=[f for _,f in agg_funcs]),
                                              axis=1, result_type='expand')

                my_logger.info('all stats computation done')

                df['map_quality'] = df.apply(lambda x: [_.mapping_quality for _ in alignment_lookup[x.name]], axis=1)
                df['map_quality_mean'] = df.map_quality.apply(lambda x: np.array(x).mean())
                df['map_quality_median'] = df.map_quality.apply(lambda x: np.quantile(
                    np.array(x).astype(int), .5))

                df['ratio_map_to_len'] = df.no_mappings/df.length

                my_logger.info('writing result to csv')
                df.to_csv(snakemake.output.csv)
            else: # dirty hack to get around an empty alignment
                cols = ['nc_accession', 'description', 'length', 'no_mappings', 'std_3',
                        'mean_3', '95_perc_3', 'std_5', 'mean_5', '95_perc_5', 'std_7',
                        'mean_7', '95_perc_7', 'read_coverage_buckets', 'breadth',
                        'map_quality', 'map_quality_mean', 'map_quality_median',
                        'ratio_map_to_len']
                t = pd.DataFrame([['nc_empty', 'empty description'] +
                              [0] * (len(cols) - 2)], columns=cols).set_index('nc_accession')
                t.to_csv(snakemake.output.csv)