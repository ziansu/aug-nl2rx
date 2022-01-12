from typing import NewType
from data_generation import merge_files
from data_generation.augmentation import parallel_augmentation
from data_generation.regex_transform import RegexTransformBeta

import pandas as pd

def test_number_parallel_aug():
    src_data_path = '/home/su284/workspace/StructuredRegex/code/datasets/'
    with open(src_data_path+'StReg/src-train.txt', 'r') as f1, open(src_data_path+'StReg/targ-train.txt', 'r') as f2:
        src_train = f1.readlines()
        targ_train = f2.readlines()
    new_src_train = []
    new_targ_train = []
    for src, targ in zip(src_train, targ_train):
        new_src, new_targ = parallel_augmentation(src, targ, ['number'])
        new_src_train.append(new_src)
        new_targ_train.append(new_targ)
    with open(src_data_path+'StReg-Aug/src-train-extra-2.txt', 'w') as f1, open(src_data_path+'StReg-Aug/targ-train-extra-2.txt', 'w') as f2:
        f1.writelines(new_src_train)
        f2.writelines(new_targ_train)

def test_regex_aug():
    rx_transform = RegexTransformBeta()
    src_data_path = '/home/su284/workspace/StructuredRegex/code/datasets/'
    with open(src_data_path+'StReg/src-train.txt', 'r') as f1, open(src_data_path+'StReg/targ-train.txt', 'r') as f2:
        src_train = f1.readlines()
        targ_train = f2.readlines()
    new_src_train = []
    new_targ_train = []
    for src, targ in zip(src_train, targ_train):
        new_targ = rx_transform.random_transform(targ.replace(' ', ''))  # no spaces
        new_targ_train.append(new_targ + '\n')

    # original src
    df = pd.DataFrame({'description': src_train, 'regex': new_targ_train, 'pos_examples': ['N/A'] * len(src_train), 'neg_examples': ['N/A'] * len(src_train)})
    df.to_csv('./syn_data/diverse_test.csv', sep='\t')

def test_regex_parallel_aug(size=1):
    """
    :param size: how big is the augmented data
    """
    src_data_path = '/home/su284/workspace/StructuredRegex/code/datasets/'
    with open(src_data_path+'StReg/src-train.txt', 'r') as f1, open(src_data_path+'StReg/targ-train.txt', 'r') as f2:
        src_train = f1.readlines()
        targ_train = f2.readlines()
    for i in range(size):
        count = 0
        failed = 0
        new_src_train = []
        new_targ_train = []
        for src, targ in zip(src_train, targ_train):
            new_src, new_targ = parallel_augmentation(src.strip(), targ.strip(), mode='regex2nl')
            count += 1
            # if count > 5:
            #     break
            if not new_src:
                failed += 1
            else:
                new_src_train.append(new_src + '\n')
                new_targ_train.append(new_targ + '\n')
        print('Failure ratio:', round(failed / count, 4))


        df = pd.DataFrame({'description': new_src_train, 'regex': new_targ_train, 'pos_examples': ['N/A'] * len(new_src_train), 'neg_examples': ['N/A'] * len(new_src_train)})
        df.to_csv('./syn_data/rx_aug_test.csv', sep='\t')

        with open(src_data_path+f'StReg-Aug/src-train-extra-3-{i}.txt', 'w') as f1, open(src_data_path+f'StReg-Aug/targ-train-extra-3-{i}.txt', 'w') as f2:
            f1.writelines(new_src_train)
            f2.writelines(new_targ_train)

    merge_files([src_data_path+'StReg/src-train.txt'] + [src_data_path+'StReg-Aug/src-train-extra-3-{}.txt'.format(i) for i in range(size)], src_data_path+'StReg-Aug/src-train.txt')
    merge_files([src_data_path+'StReg/targ-train.txt'] + [src_data_path+'StReg-Aug/targ-train-extra-3-{}.txt'.format(i) for i in range(size)], src_data_path+'StReg-Aug/targ-train.txt')
    
if __name__ == '__main__':
    # test_number_parallel_aug()
    # test_regex_aug()
    test_regex_parallel_aug(3)