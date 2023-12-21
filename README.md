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
