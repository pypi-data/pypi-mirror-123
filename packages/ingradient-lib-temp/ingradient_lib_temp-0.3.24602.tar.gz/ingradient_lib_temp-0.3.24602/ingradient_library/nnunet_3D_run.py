from ingradient_library.dataloads import *
from ingradient_library.preprocessing import Normalizer
from ingradient_library.dataloads import DataLoader3D
from ingradient_library.dataloads import CustomDataset
from ingradient_library.preprocessing import Resampling
from ingradient_library.preprocessing import Normalizer
from ingradient_library.preprocessing import Get_target_spacing
from ingradient_library.transform import Transform
from ingradient_library.get_nnunet_setting import get_transform_params
from ingradient_library.deep_supervision_loss import *
from ingradient_library.trainer import Trainer
from ingradient_library.model import *
from ingradient_library.model import *
from ingradient_library.get_information import get_imbalance_weight
from ingradient_library.optimizer import SAMSGD
from torch.utils.data.dataset import random_split
from ingradient_library.get_information import get_imbalance_weight
import torch.optim as optim
import torch.nn as nn


def nnunet_3D_run(LOAD_PATH, SAVE_MODEL_PATH, GPU_DEVICE_INDEX, patch_size, batch_size, n_classes, n_modalities):
    transform = Transform(*get_transform_params(GPU_DEVICE_INDEX))
    dataset = CustomDataset(LOAD_PATH, normalizer = Normalizer())
    tr_dataset, val_dataset = random_split(dataset, [len(dataset) - len(dataset)//9, len(dataset)//9])
    tr_dataloader = DataLoader3D(tr_dataset, patch_size = patch_size, device = GPU_DEVICE_INDEX, batch_size = batch_size, transform = transform)
    val_dataloader = DataLoader3D(val_dataset, patch_size = patch_size, device = GPU_DEVICE_INDEX, batch_size = batch_size)
    weight = get_imbalance_weight(LOAD_PATH, n_classes)

    model = Deep_Supervision_UNet3d(patch_size = patch_size, n_modalities = n_modalities, final_output_channels = n_classes, is_binary = False).to(GPU_DEVICE_INDEX)
    loss2 = Multi_Dice_Loss(n_classes)
    loss1 = nn.CrossEntropyLoss(reduction = 'none', weight = torch.tensor(weight).float().to(GPU_DEVICE_INDEX))
    optimizer = optim.Adam(model.parameters(), lr = 0.1)
    scheduler = optim.lr_scheduler.LambdaLR(optimizer=optimizer,
                                lr_lambda=lambda epoch: 0.95 ** epoch)
    trainer = Trainer(tr_dataloader = tr_dataloader, val_dataloader= val_dataloader, model =  model, optimizer = optimizer, scheduler = scheduler, losses = [loss1, loss2], save_path = SAVE_MODEL_PATH, is_deep_supervision = True)
    trainer.run()



def nnunet_3D_run_narrow(LOAD_PATH, SAVE_MODEL_PATH, GPU_DEVICE_INDEX, patch_size, batch_size, n_classes, n_modalities):
    transform = Transform(*get_transform_params(GPU_DEVICE_INDEX))
    dataset = CustomDataset(LOAD_PATH, normalizer = Normalizer())
    tr_dataset, val_dataset = random_split(dataset, [len(dataset) - len(dataset)//9, len(dataset)//9])
    tr_dataloader = DataLoader3D(tr_dataset, patch_size = patch_size, device = GPU_DEVICE_INDEX, batch_size = batch_size, transform = transform)
    val_dataloader = DataLoader3D(val_dataset, patch_size = patch_size, device = GPU_DEVICE_INDEX, batch_size = batch_size)
    weight = get_imbalance_weight(LOAD_PATH, n_classes)

    model = Deep_Supervision_UNet3d_Narrow(patch_size = patch_size, n_modalities = n_modalities, final_output_channels = n_classes, is_binary = False).to(GPU_DEVICE_INDEX)
    loss2 = Multi_Dice_Loss(n_classes)
    loss1 = nn.CrossEntropyLoss(reduction = 'none', weight = torch.tensor(weight).float().to(GPU_DEVICE_INDEX))
    optimizer = optim.Adam(model.parameters(), lr = 0.1)
    scheduler = optim.lr_scheduler.LambdaLR(optimizer=optimizer,
                                lr_lambda=lambda epoch: 0.95 ** epoch)
    trainer = Trainer(tr_dataloader = tr_dataloader, val_dataloader= val_dataloader, model =  model, optimizer = optimizer, scheduler = scheduler, losses = [loss1, loss2], save_path = SAVE_MODEL_PATH, is_deep_supervision = True)
    trainer.run()