import oneflow as flow
import torch

def convert_torch_to_flow(model, torch_weight_path, save_path):
    parameters = torch.load(torch_weight_path)
    new_parameters = dict()
    for key, value in parameters.items():
        if "num_batches_tracked" not in key:
          val = value.detach().cpu().numpy()
          new_parameters[key] = val
    model.load_state_dict(new_parameters)
    flow.save(model.state_dict(), save_path)
