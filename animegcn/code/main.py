from animegcn.code.register import dataset
import animegcn.code.register
import animegcn.code.world
import animegcn.code.utils
from animegcn.code.world import cprint
import torch
import numpy as np
import time
import animegcn.code.Procedure
from os.path import join
# ==============================
animegcn.code.utils.set_seed(animegcn.code.world.seed)
print(">>SEED:", animegcn.code.world.seed)
# ==============================

Recmodel = animegcn.code.register.MODELS[animegcn.code.world.model_name](
    animegcn.code.world.config, dataset)
Recmodel = Recmodel.to(animegcn.code.world.device)
bpr = animegcn.code.utils.BPRLoss(Recmodel, animegcn.code.world.config)

weight_file = r'./animegcn/lgn-anime-3-512.pth.tar'

Recmodel.load_state_dict(torch.load(
    weight_file, map_location=torch.device('cpu')))
animegcn.code.world.cprint(f"loaded model weights from {weight_file}")


def call_inference(user):
    return animegcn.code.Procedure.Infer(dataset, Recmodel, user)


if __name__ == "__main__":
    print("Inferring on predict:")
    animegcn.code.Procedure.Infer(dataset, Recmodel, 5373)
