'''
Created on Mar 1, 2020
Pytorch Implementation of LightGCN in
Xiangnan He et al. LightGCN: Simplifying and Powering Graph Convolution Network for Recommendation

@author: Jianbai Ye (gusye@mail.ustc.edu.cn)
'''

from warnings import simplefilter
import sys
import os
from os.path import join
import torch
from enum import Enum
import multiprocessing

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

ROOT_PATH = "/animegcn/"
CODE_PATH = join(ROOT_PATH, 'code')
DATA_PATH = join(ROOT_PATH, 'data')
BOARD_PATH = join(CODE_PATH, 'runs')
FILE_PATH = join(CODE_PATH, 'checkpoints')
sys.path.append(join(CODE_PATH, 'sources'))

config = {}
all_dataset = ['anime']
all_models = ['mf', 'lgn']
# config['batch_size'] = 4096
config['bpr_batch_size'] = 2048
config['latent_dim_rec'] = 512
config['lightGCN_n_layers'] = 3
config['dropout'] = 0
config['keep_prob'] = 0.6
config['A_n_fold'] = 100
config['test_u_batch_size'] = 100
config['multicore'] = 0
config['lr'] = 0.001
config['decay'] = 1e-4
config['pretrain'] = 0
config['A_split'] = False
config['bigdata'] = False
config['mode'] = 'infer'

GPU = torch.cuda.is_available()
device = torch.device('cuda' if GPU else "cpu")
CORES = multiprocessing.cpu_count() // 2
seed = 2020

dataset = 'anime'
model_name = 'lgn'
if dataset not in all_dataset:
    raise NotImplementedError(
        f"Haven't supported {dataset} yet!, try {all_dataset}")
if model_name not in all_models:
    raise NotImplementedError(
        f"Haven't supported {model_name} yet!, try {all_models}")

TRAIN_epochs = 10
LOAD = 1
PATH = "./animegcn/data/anime"
topks = 40
tensorboard = 0
comment = 'lgn'
# let pandas shut up
simplefilter(action="ignore", category=FutureWarning)


def cprint(words: str):
    print(f"\033[0;30;43m{words}\033[0m")
