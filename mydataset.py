import torch
pretrained_weights  = torch.load('models/preTrainedModels/detr-r50-e632da11.pth')

num_class = 23    #类别数+1，1为背景
pretrained_weights["model"]["class_embed.weight"].resize_(num_class+1, 256)
pretrained_weights["model"]["query_embed.weight"].resize_(50,256)
pretrained_weights["model"]["class_embed.bias"].resize_(num_class+1)
torch.save(pretrained_weights, "detr-r50_%d_query25.pth"%num_class)
