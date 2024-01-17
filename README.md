# PMB5.0.0

## Table of Contents
1. [Overview](##Overview)
2. [Dataset Description](#Dataset-Description)
3. [Experiments](##experiment)
4. [License](##License)
5. [Contributors](##Contributors)

## Overview
PMB release 5.0.0. Compared to release 4.0.0, the following addition/changes have been made:

* Switching from clause notation to sequence notation (SBN) for meaning representation
* Adding Chinese and Japanese data to the existing languages
* Replacing Bronze data with Copper data in nl, de, it and ja
* Reorganizing the train/development/test sets based on length distribution
* Reconstruct the structure of split sets and reformat the .sbn file in the format of ID/raw/sbn
* In this github repo, we provide the seq2seq data. For more detailed data, see https://pmb.let.rug.nl/releases/

## Dataset Description

Training a DRS(SBN) parser using PMB data. We have:
* gold data, human annotated data
* silver data, partially human annotated data
* bronze data, mechine generated data
* copper data, THIS IS NEW IN PMB5.0.0. For low resource languages(nl, de, it), we replace their bronze data with English bronze data. We call this part as copper.
* The following is the statistics of the gold, silver and bronze data. For English, we split it in 8:1:1. For the others, we split in 4:3:3 to ensure the test is enough.

|            |    Gold-Train |    Gold-Dev  |    Gold-Test |   Silver     |   Bronze    |   Copper     |
|------------|---------------|--------------|--------------|--------------|-------------|--------------|
| English    |      9057     |     1132     |      1132    |    143731    |     14425   |              |
| German     |      1206     |      900     |       900    |      6862    |    150682   |     150493   |
| Dutch      |       586     |      435     |       435    |      1646    |     27856   |      27840   |
| Italian    |       745     |      555     |       555    |      4316    |     92413   |      92394   |


## Experiments
Here we provide the results for parsing:

| Parser   | English F1 | ERR | Dutch F1 | ERR | Italian F1 | ERR | German F1 | ERR |
|----------|------------|-----|----------|-----|------------|-----|-----------|-----|
| LSTM     | 78.6       | 8.4 | 80.2     | 4.0 | 74.4       | 8.5 | 79.6      | 5.0 |
| mT5      | 88.8       | 2.8 | 86.7     | 1.9 | 47.0       | 16.0| 82.0      | 2.8 |
| byT5     | 91.4       | 2.1 | 88.0     | 0.7 | 79.8       | 5.0 | 87.2      | 0.7 |
| mBART    | 89.1       | 2.3 | 86.1     | 1.8 | 64.5       | 3.4 | 86.2      | 1.8 |
| DRS-MLM  | 91.5       | 1.5 | 87.1     | 2.1 | 85.5       | 2.0 | 87.2      | 0.9 |


## Model Usage
run the following command to use pre-trained mBart model by [Chunliu and Huiyuan](https://github.com/wangchunliu/DRS-pretrained-LMM)

    python3 src/model/mBART/run.py

run the following command to use pre-trained byT5 model,

    python3 src/model/byT5/run.py

Please go to the args to see more hyperparameters and add any if you want.

## Evaluation
we use the SMATCH score to evaluate the results:
see the decription in folder: data/pmb-5.0.0/src/sbn

## License

## Contributors
Xiao Zhang, Chunliu Wang, Rik van Noord, Johan Bos
