#!/bin/bash

languages=("en" "de" "nl" "it" "ja")
data_types=("gold" "silver" "bronze")
folders=("train" "test" "dev")
log_file="./output.log"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)" 
release_dir="$script_dir/../../"

echo "$release_dir"

for lang in "${languages[@]}"; do
  for data_type in "${data_types[@]}"; do
    echo "Running standard_split.py with -l $lang -d $data_type"
    python3 "$script_dir/standard_split.py" -r "$release_dir/data/" -o "$release_dir/split" -l "$lang" -d "$data_type" -sk "$script_dir/long_ind.txt" -s True >> "$log_file" 2>&1
    for folder in "${folders}"; do
      if [ "$folder"=="train" ]; then
        echo "random shuffle train file, seed 32"
        python3 "$script_dir/shuffle.py" -r "$release_dir/split/$lang/$folder/$data_type.sbn" -o "$release_dir/split/$lang/$folder/$data_type.sbn" -rs 32 >> "$log_file" 2>&1
      elif [ "$folder"=="dev" ]; then
        echo "random shuffle dev file, seed 42"
        python3 "$script_dir/shuffle.py" -r "$release_dir/split/$lang/$folder/$data_type.sbn" -o "$release_dir/split/$lang/$folder/$data_type.sbn" -rs 42 >> "$log_file" 2>&1
      elif [ "$folder"=="test" ]; then
        echo "random shuffle test file, seed 52"
        python3 "$script_dir/shuffle.py" -r "$release_dir/split/$lang/$folder/$data_type.sbn" -o "$release_dir/split/$lang/$folder/$data_type.sbn" -rs 52 >> "$log_file" 2>&1
      else
        echo "something wrong"
      fi
    done
  done
  mv "$release_dir/split/$lang/test/gold.sbn" "$release_dir/split/$lang/test/standard.sbn"
  mv "$release_dir/split/$lang/dev/gold.sbn" "$release_dir/split/$lang/dev/standard.sbn"
done


for lang in "${languages[@]}"; do
  mv "$release_dir/split/$lang/test/gold.sbn" "$release_dir/split/$lang/test/standard.sbn"
  mv "$release_dir/split/$lang/dev/gold.sbn" "$release_dir/split/$lang/dev/standard.sbn"
done

python3 long.py -r "$release_dir/data/" -o "$release_dir/split/" -l en -li "$release_dir/src/split/long_ind.txt"

for lang in "${languages[@]}"; do
    echo "Checking duplicates $lang test with silver/bronze train"
    python3 "$script_dir/check_duplicates.py" -f1 "$release_dir/split/$lang/test/standard.sbn" -f2 "$release_dir/split/$lang/train/silver.sbn" -o "$release_dir/split/$lang/train/silver.sbn"  >> "$log_file" 2>&1
    python3 "$script_dir/check_duplicates.py" -f1 "$release_dir/split/$lang/test/standard.sbn" -f2 "$release_dir/split/$lang/train/bronze.sbn" -o "$release_dir/split/$lang/train/bronze.sbn"  >> "$log_file" 2>&1
done

copper_languages=("nl" "de" "it" "ja")

for lang in "${copper_languages[@]}"; do
  echo "Running copper.py with -l $lang"
  python3 "$script_dir/copper.py" -r "$release_dir/data" -o "$release_dir/split" -l "$lang" >> "$log_file" 2>&1
  rm "$release_dir/split/$lang/train/bronze.sbn"
done

python3 check_empty.py
