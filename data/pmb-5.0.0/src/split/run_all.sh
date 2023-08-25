#!/bin/bash

languages=("en")
data_types=("gold")
log_file="./output1.log"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" 
split_dir="$script_dir/../../split"

for lang in "${languages[@]}"; do
  for data_type in "${data_types[@]}"; do
    echo "Running standard_split.py with -l $lang -d $data_type"
    python3 "$script_dir/standard_split.py" -r "$split_dir/data/" -o "$split_dir/split" -l "$lang" -d "$data_type" -sk "$script_dir/long_ind.txt" -s True >> "$log_file" 2>&1
  done
done

for lang in "${languages[@]}"; do
    echo "Checking duplicates $lang test with silver/bronze train"
    mv "$split_dir/$lang/test/gold.txt.sbn" "$split_dir/$lang/test/standard.txt.sbn"
    python3 "$script_dir/check_duplicates.py" -f1 "$split_dir/$lang/test/standard.txt.sbn" -f2 "$split_dir/$lang/train/silver.txt.sbn" -o "$split_dir/$lang/train/silver.txt.sbn"  >> "$log_file" 2>&1
    python3 "$script_dir/check_duplicates.py" -f1 "$split_dir/$lang/test/standard.txt.sbn" -f2 "$split_dir/$lang/train/bronze.txt.sbn" -o "$split_dir/$lang/train/bronze.txt.sbn"  >> "$log_file" 2>&1
done

