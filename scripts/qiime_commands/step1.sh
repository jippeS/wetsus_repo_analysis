#!/bin/bash

#folder_path = $1
#metadata = $2
#forward_primer_seq = $3
#reverse_primer_seq = $4
#name_convention_PairEndSequences = $5
#outputdir = $6

python3 wetsus_repo_analysis/scripts/pre_data.py "$1/"
mkdir -p "$1/input/raw_data"
mv "$1/input/"*.fastq "$1/input/raw_data/"
mv "$1/input/"*.txt "$1/input/$2"
mkdir "$1/output/"
python3 wetsus_repo_analysis/scripts/pre_demux.py --inputdir="$1/" --forward="$3" --reverse="$4"
gzip -c "$1/input/raw_data/forward.fastq" > "$1/input/raw_data/forward.fastq.gz"
gzip -c "$1/input/raw_data/reverse.fastq" > "$1/input/raw_data/reverse.fastq.gz"
rm "$1"/input/raw_data/*.fastq
qiime tools import --type MultiplexedPairedEndBarcodeInSequence --input-path "$1/input/raw_data/" --output-path "$6/$5"
