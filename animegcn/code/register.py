import animegcn.code.world
import animegcn.code.dataloader
import animegcn.code.model
import animegcn.code.utils
from pprint import pprint

if animegcn.code.world.dataset in ['anime']:
    dataset = animegcn.code.dataloader.Loader(
        path="../data/"+animegcn.code.world.dataset)

print('===========config================')
pprint(animegcn.code.world.config)
print("cores for test:", animegcn.code.world.CORES)
print("comment:", animegcn.code.world.comment)
print("LOAD:", animegcn.code.world.LOAD)
print("Weight path:", animegcn.code.world.PATH)
print("Test Topks:", animegcn.code.world.topks)
print("using bpr loss")
print('===========end===================')

MODELS = {
    'lgn': animegcn.code.model.LightGCN
}
