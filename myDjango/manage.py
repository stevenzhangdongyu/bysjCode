#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import json
import os
import sys

import torch
import torchvision

model = None
CLASSES = None
image_Totensor = None
imagenet_class_index = None
def initGlobal():
    global CLASSES
    CLASSES = ["road-signs","bus_stop","do_not_enter","do_not_stop","do_not_turn_l","do_not_turn_r","do_not_u_turn",
    "enter_left_lane","green_light","left_right_lane","no_parking","parking","ped_crossing",
    "ped_zebra_cross","railway_crossing","red_light","stop","t_intersection_l","traffic_light",
    "u_turn","warning","yellow_light",
    ]
    global model
    model = torch.load('mobile_model.pt')
    # Since we are using our model only for inference, switch to `eval` mode:
    model.eval()
    global image_Totensor
    image_Totensor = torchvision.transforms.ToTensor()
    global imagenet_class_index
    imagenet_class_index  = json.load(open('F:\\桌面学习资料\\毕业设计\\code\\detr\\imagenet_class_index.json'))
def main():
    initGlobal()
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myDjango.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
