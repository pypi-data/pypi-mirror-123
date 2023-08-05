import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from torchvision.transforms import transforms
from tqdm import tqdm
import numpy as np

class ImageNetDataLoader(DataLoader):
    def __init__(self, data_dir, split='train', image_size=224, batch_size=16, num_workers=8):

        if split == 'train':
            transform = transforms.Compose([
                transforms.Resize((image_size, image_size)),
                transforms.RandomHorizontalFlip(),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ])
        else:
            transform = transforms.Compose([
                transforms.Resize(256, interpolation=2),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
            ])

        self.dataset = ImageFolder(root=os.path.join(data_dir, split), transform=transform)
        super(ImageNetDataLoader, self).__init__(
            dataset=self.dataset,
            batch_size=batch_size,
            shuffle=True if split == 'train' else False,
            num_workers=num_workers)


def setup_device(n_gpu_use):
    n_gpu = torch.cuda.device_count()
    if n_gpu_use > 0 and n_gpu == 0:
        print("Warning: There\'s no GPU available on this machine, training will be performed on CPU.")
        n_gpu_use = 0
    if n_gpu_use > n_gpu:
        print("Warning: The number of GPU\'s configured to use is {}, but only {} are available on this machine.".format(n_gpu_use, n_gpu))
        n_gpu_use = n_gpu
    device = torch.device('cuda:0' if n_gpu_use > 0 else 'cpu')
    list_ids = list(range(n_gpu_use))
    return device, list_ids


def accuracy(output, target, topk=(1,)):
    """Computes the precision@k for the specified values of k"""""
    maxk = max(topk)
    batch_size = target.size(0)

    _, pred = output.topk(maxk, 1, True, True)
    pred = pred.t()
    correct = pred.eq(target.view(1, -1).expand_as(pred))

    res = []
    for k in topk:
        correct_k = correct[:k].contiguous().view(-1).float().sum(0)
        res.append(correct_k / batch_size * 100.0)
    return res


def eval_torch_acc(model, data_dir, pretrained_path=None, n_gpu_use=1, batch_size=32, img_size=224):
    device, device_ids = setup_device(n_gpu_use)

    if pretrained_path:
        state_dict = torch.load(pretrained_path)
        model.load_state_dict(state_dict)
        print("Load pretrained weights from {}".format(pretrained_path))

    model = model.to(device)
    if len(device_ids) > 1:
        model = torch.nn.DataParallel(model, device_ids=device_ids)

    data_loader = ImageNetDataLoader(
        data_dir = data_dir,
        image_size = img_size,
        batch_size = batch_size,
        num_workers = 8,
        split='val'
    )
    total_batch = len(data_loader)

    print("Start Evaluation")
    acc1s = []
    acc5s = []
    model.eval()
    with torch.no_grad():
        pbar = tqdm(enumerate(data_loader), total=total_batch)
        for batch_idx, (data, target) in pbar:
            pbar.set_description("Batch {:05d}/{:05d}".format(batch_idx, total_batch))

            data = data.to("cuda")
            target = target.to("cuda")

            pred_logits = model(data)
            acc1, acc5 = accuracy(pred_logits, target, topk=(1, 5))

            acc1s.append(acc1.item())
            acc5s.append(acc5.item())

            pbar.set_postfix(acc1=acc1.item(), acc5=acc5.item())
        
    print("Evaluation on dataset {:s}, Acc@1: {:.4f}, Acc@5: {:.4f}".format("ImageNet", np.mean(acc1s), np.mean(acc5s)))
