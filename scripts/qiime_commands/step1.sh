#!/bin/bash

folder_path = $1
metadata = $2
forward_primer_seq = $3
reverse_primer_seq = $4
name_convention_PairEndSequences = $5

python3 wetsus_repo_analysis/scripts/pre_data.py "$folder_path/"
mkdir -p "$folder_path/input/raw_data"
mv "$folder_path/input/*.fastq" "$folder_path/input/raw_data/"
mv "$folder_path/input/*.txt" "$folder_path/input/$metadata"
mkdir "$folder_path/output/"
python3 wetsus_repo_analysis/scripts/pre_demux.py --inputdir="$folder_path/" --forward="$forward_primer_seq" --reverse="$reverse_primer_seq"
gzip -c "$folder_path/input/raw_data/forward.fastq" > "$folder_path/input/raw_data/forward.fastq.gz"
gzip -c "$folder_path/input/raw_data/reverse.fastq" > "$folder_path/input/raw_data/reverse.fastq.gz"
rm "$folder_path/input/raw_data/*.fastq"
qiime tools import --type MultiplexedPairedEndBarcodeInSequence --input-path "$folder_path/$folder_name/input/raw_data/" --output-path "$outputdir/$name_convention_PairEndSequences"
