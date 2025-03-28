# import os
from pathlib import Path
import polars as pl
import pysam
import logging

### load config ###
config_path = '~/mutationalscanning/Workspaces/chcharlton/kinetics/scripts/linear_ipd_retrieval/ob006.ini'

from config import load_config, PROCESSED_DATA_DIR

config = load_config('ob006-run0.ini')

bam_path = Path(config['Paths']['bam_filepath']).expanduser()
bed_path = Path(config['Paths']['bed_path']).expanduser()
results_path = Path(config['Paths']['output_dir']).expanduser()
context = int(config['Constants']['context'])




# enable logging 
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_bed_file(bed_path):
    """Loads a bed file into a Polars dataframe and validates it"""
    logging.info(f"Loading BED file: {bed_path}")  # Log the *expanded* path
    if not bed_path.exists(): 
        raise FileNotFoundError(f"BED file not found at: {bed_path}")
    try:
        df = pl.read_csv(bed_path, separator="\t").drop_nulls()
        required_columns = ['strand', 'contig', 'start', 'end', 'position_in_read', 'read_name']
        for column in required_columns:
            assert column in df.columns, f"Column {column} not found in BED file"
        return df
    except Exception as e:
        raise

# load the bed file with observed mutations into a DF
df = load_bed_file(bed_path)



# load the kinetics data for ob006 with pysam

def get_kinetic_data(
    row: tuple, header: list, bam: pysam.AlignmentFile, context: int
) -> tuple[list | None, list | None, list | None]:
    """
    Retrieves selected kinetics and nucleotide data for a single read from an open pysam AlignmentFile.
    
    Args:
        row: A tuple representing a single row of a Polars DataFrame.
        header: A list of column names corresponding to the row.
        bam: An open pysam.AlignmentFile object.
        context: The number of bases to include on either side of the mutation 
                 (total size = 2*context + 1).
    
    Returns:
        A tuple: (unique_id, ipd_fwd, ipd_rev, base_pairs, fn, rn)
        where ipd_fwd is a list of IPD values for the forward strand,
              ipd_rev is a list of IPD values for the reverse strand,
              base_pairs is a list of base pairs centered on the mutation,
              fn and rn are additional tag values.
        If any error occurs or the data is invalid, returns a tuple of None values.
    """
    unique_id = row[header.index("unique_id")]
    contig = row[header.index("contig")]
    start = int(row[header.index("start")])
    end = int(row[header.index("end")])
    position_in_read = int(row[header.index("position_in_read")])
    read_name = row[header.index("read_name")]
    null_data = (None, None, None, None, None, None)

    # Compute slice indices for the forward and reverse strands.
    fwd_start = position_in_read - context
    fwd_end = position_in_read + context + 1
    rev_start = -(position_in_read + 1) - context
    rev_end = -(position_in_read + 1) + context + 1

    def get_tag_slice(read, tag: str, start: int, end: int) -> list | None:
        """Safely retrieves and slices a tag from a read."""
        try:
            tag_value = read.get_tag(tag)
            return list(tag_value[start:end])
        except (KeyError, IndexError) as e:
            logging.warning("Error getting tag '%s' for read %s: %s", tag, read_name, e)
            return None

    # Find the matching read using a generator expression for elegance.
    try:
        matching_read = next(
            read
            for read in bam.fetch(contig=contig, start=start, end=end)
            if read.query_name == read_name
        )
    except StopIteration:
        return null_data
    except ValueError as e:
        logging.error("Error during bam.fetch for read %s: %s", read_name, e)
        return null_data

    # Determine the appropriate tags based on the strand orientation.
    fwd_tag, rev_tag = (("ri", "fi") if matching_read.is_reverse else ("fi", "ri"))

    # Retrieve the IPD values using our helper function.
    ipd_fwd = get_tag_slice(matching_read, fwd_tag, fwd_start, fwd_end)
    ipd_rev = get_tag_slice(matching_read, rev_tag, rev_start, rev_end)
    if ipd_fwd is None or ipd_rev is None:
        return null_data

    # Retrieve additional tags.
    try:
        fn = matching_read.get_tag("fn")
        rn = matching_read.get_tag("rn")
    except KeyError as e:
        logging.warning("Read %s missing tag: %s", read_name, e)
        return null_data

    # Retrieve nucleotide sequence centered on the mutation.
    base_pairs = list(matching_read.query_sequence[fwd_start:fwd_end])
    expected_length = 2 * context + 1
    if not (len(ipd_fwd) == len(ipd_rev) == len(base_pairs) == expected_length):
        logging.warning(
            "Unexpected length for read %s: expected %d, got fwd:%d, rev:%d, bases:%d",
            read_name,
            expected_length,
            len(ipd_fwd),
            len(ipd_rev),
            len(base_pairs),
        )
        return null_data

    return unique_id, ipd_fwd, ipd_rev, base_pairs, fn, rn
 
def process_kinetics(df: pl.DataFrame, bam_path: Path, context: int) -> pl.DataFrame:
    """Retrieve and store the kinetics data for all reads in the DataFrame."""
    if not bam_path.exists():
        raise FileNotFoundError(f"BAM file not found: {bam_path}")

    # try:
    with pysam.AlignmentFile(bam_path, 'rb') as bam:
        # Prepare the data for apply.  Extract only necessary columns *before* the apply.
        cols = ['unique_id', 'contig','start', 'end', 'position_in_read', 'read_name']
        subset_df = df.select(cols)
        # map rows applies the get_kinetics data function to all the r
        results = subset_df.map_rows(lambda row: get_kinetic_data(row=row, header=cols, bam=bam, context=context))
        results.columns = ['unique_id', 'ipd_fwd', 'ipd_rev', 'base_pairs', 'fn', 'rn']
        # Join with the original DataFrame based on row index.  Create index columns first.
        df = df.with_row_index('row_index')

    return results



def main():
    # try:
    df = load_bed_file(bed_path)
    logging.info(f"Loaded BED file: {bed_path}")

    final_df = process_kinetics(df, bam_path, context)
    logging.info("retrieval complete")
    output_path = results_path / config_path + '.parquet'
    final_df.write_parquet(output_path)

    # except Exception as e:
    #     logging.error(f"An error occurred: {e}


if __name__ == "__main__":
    main()
