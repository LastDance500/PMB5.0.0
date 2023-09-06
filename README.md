# PMB5.0.0

## Table of Contents
1. [Overview](##Overview)
2. [Dataset Description](#Dataset-Description)
3. [Usage](##Usage)
4. [Experiments](##experiment)
5. [License](##License)
6. [Contributors](##Contributors)

## Overview
Parallel Meaning Bank 5.0.0

Results under old sbn-conversion, compasing with 4.0.0 results in brackets. (will be updated under new sbn conversion) 30-08-2023
| Model       |      en        |    en(long)    |        de        |       nl        |        it        |
|-------------|----------------|----------------|------------------|-----------------|------------------|
| mBart       |   93.9 (94.7)  |      10.0      |    91.6 (91.3)   |   92.2 (88.2)   |     90.5(90.9)   |
| NeuralBoxer |   81.1 (92.5)  |      23.5      |    85.1 (74.7)   |   78.7 (71.6)   |     84.3(75.4)   |


Results under new sbn-conversion!!  05-09-2023
| Model       |      en        |    en(long)    |        de        |       nl        |        it        |
|-------------|----------------|----------------|------------------|-----------------|------------------|
| mBart       |     91.4       |      TBA       |        87.6      |       88.0      |        86.0      |
| NeuralBoxer |     79.1       |      TBA       |        81.1      |       74.4      |        80.6      |


Results under smatch (remove TOP label)  06-09-2023
| Model       |      en        |    en(long)    |        de        |       nl        |        it        |
|-------------|----------------|----------------|------------------|-----------------|------------------|
| mBart       |     91.0       |      TBA       |        86.9      |       87.4      |        85.3      |
| NeuralBoxer |     78.6       |      TBA       |        80.2      |       73.3      |        79.6      |

Results under smatch (remove Top label, de/nl/it train on bronze rather than copper) 06-09-2023
| Model       |        de        |       nl        |        it        |
|-------------|------------------|-----------------|------------------|
| mBart       |        85.7      |       85.9      |        86.3      |
| NeuralBoxer |        TBA       |       TBA       |        TBA       |

PMB5.0.0 training statistics

|            |    Gold-Train |    Gold-Dev  |    Gold-Test |   Silver     |   Bronze    |   Copper     |
|------------|---------------|--------------|--------------|--------------|-------------|--------------|
| English    |      9057     |     1132     |      1132    |    143731    |     14425   |              |
| German     |      1206     |      900     |       900    |      6862    |    150682   |     150493   |
| Dutch      |       586     |      435     |       435    |      1646    |     27856   |      27840   |
| Italian    |       745     |      555     |       555    |      4316    |     92413   |      92394   |




## Dataset Description

### General Information
- **Purpose**: 
- **Dataset Version**: 5.0.0
- **Data Format**:

### Metadata
- **Time period**:
- **Data Source**: 
- **Data Quality**:

## Experiments
mBART & NeuralBoxer can be found at

    src/model/$Model/result


## Model Usage
run the following command to use pre-trained mBart model by [Chunliu and Huiyuan](https://github.com/wangchunliu/DRS-pretrained-LMM)

    python3 src/model/mBART/run.py


## Contributors
Xiao Zhang, Chunliu Wang, Rik van Noord, Johan Bos
