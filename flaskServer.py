import random
import time
import datetime
from minio import Minio
import cv2
from urllib.parse import urlparse
import os
import numpy as np
import torch
import torchvision
from flask import Flask, jsonify, render_template, send_file
from flask_cors import CORS
from torchvision.ops import batched_nms

app = Flask(__name__,template_folder='templates')
client = Minio(
    "116.63.35.72:9000",
    access_key="cLuAvJjxwX7PJs7IUzRL",
    secret_key="80pT8fpk4DAtWqRSK4tEu5hyU5ho7EQQTAcpXag8",
    secure=False
)
IMAGES = [

]
bucket_name = "imagebucket"
objects = client.list_objects("imagebucket",prefix='test2017/')
for obj in objects:
    url = client.presigned_get_object(bucket_name,obj.object_name)
    IMAGES.append(url)
def allow_cors(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        response.headers.add('Access-Control-Allow-Origin', '*')  # 允许所有域名访问，可自定义
        return response
    return wrapper
CORS(app)

def allow_cors(func):
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        response.headers.add('Access-Control-Allow-Origin', '*')  # 允许所有域名访问，可自定义
        return response

    return wrapper
import io

import torchvision.transforms as transforms
from PIL import Image
resultBucketName = "resultbucket"
def transform_image(image_bytes):
    my_transforms = transforms.Compose([transforms.Resize(255),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])
    image = Image.open(io.BytesIO(image_bytes))
    return my_transforms(image).unsqueeze(0)
model =torch.load('mobile_model.pt')
model.eval()
image_Totensor = torchvision.transforms.ToTensor()
import json

imagenet_class_index = json.load(open('imagenet_class_index.json'))
def rescale_bboxes(out_bbox, size):
    # 把比例坐标乘以图像的宽和高，变成真实坐标
    img_w, img_h = size
    b = box_cxcywh_to_xyxy(out_bbox)
    b = b * torch.tensor([img_w, img_h, img_w, img_h], dtype=torch.float32)
    return b
def box_cxcywh_to_xyxy(x):
    # 将DETR的检测框坐标(x_center,y_cengter,w,h)转化成coco数据集的检测框坐标(x0,y0,x1,y1)
    x_c, y_c, w, h = x.unbind(1)
    b = [(x_c - 0.5 * w), (y_c - 0.5 * h),
         (x_c + 0.5 * w), (y_c + 0.5 * h)]
    return torch.stack(b, dim=1)
def filter_boxes(scores, boxes, confidence=0.7, apply_nms=True, iou=0.5):
    # 筛选出真正的置信度高的框
    keep = scores.max(-1).values > confidence
    scores, boxes = scores[keep], boxes[keep]

    if apply_nms:
        top_scores, labels = scores.max(-1)
        keep = batched_nms(boxes, top_scores, labels, iou)
        scores, boxes = scores[keep], boxes[keep]

    return scores, boxes
# COCO classes
CLASSES = [
"road-signs","bus_stop","do_not_enter","do_not_stop","do_not_turn_l","do_not_turn_r","do_not_u_turn",
"enter_left_lane","green_light","left_right_lane","no_parking","parking","ped_crossing",
"ped_zebra_cross","railway_crossing","red_light","stop","t_intersection_l","traffic_light",
"u_turn","warning","yellow_light",
]
def plot_one_box(x, img, color=None, label=None, line_thickness=1):
    # 把检测框画到图片上
    tl = line_thickness or round(0.002 * (img.shape[0] + img.shape[1]) / 2) + 1  # line/font thickness
    color = color or [random.randint(0, 255) for _ in range(3)]
    c1, c2 = (int(x[0]), int(x[1])), (int(x[2]), int(x[3]))
    cv2.rectangle(img, c1, c2, color, thickness=tl, lineType=cv2.LINE_AA)
    if label:
        tf = max(tl - 1, 1)  # font thickness
        t_size = cv2.getTextSize(label, 0, fontScale=tl / 3, thickness=tf)[0]
        c2 = c1[0] + t_size[0], c1[1] - t_size[1] - 3
        cv2.rectangle(img, c1, c2, color, -1, cv2.LINE_AA)  # filled
        cv2.putText(img, label, (c1[0], c1[1] - 2), 0, tl / 3, [225, 255, 255], thickness=tf, lineType=cv2.LINE_AA)
def get_last_part_of_url(url):
    # 解析 URL
    parsed_url = urlparse(url)
    # 获取路径的最后一个部分
    last_part = os.path.basename(parsed_url.path)
    return last_part
def get_prediction(imgUrl,name):
    image = Image.open(io.BytesIO(imgUrl))
    image_tensor = image_Totensor(image)
    image_tensor = torch.reshape(image_tensor,
                                 [-1, image_tensor.shape[0], image_tensor.shape[1], image_tensor.shape[2]])
    # image_tensor = image_tensor.to('cuda')
    time1 = time.time()
    inference_result = model(image_tensor)
    time2 = time.time()
    print("inference_time:", time2 - time1)
    probas = inference_result['pred_logits'].softmax(-1)[0, :, :-1].cpu()
    bboxes_scaled = rescale_bboxes(inference_result['pred_boxes'][0,].cpu(),
                                   (image_tensor.shape[3], image_tensor.shape[2]))
    scores, boxes = filter_boxes(probas, bboxes_scaled)
    scores = scores.data.numpy()
    boxes = boxes.data.numpy()
    image = np.array(image)
    for i in range(boxes.shape[0]):
        class_id = scores[i].argmax()
        label = CLASSES[class_id]
        confidence = scores[i].max()
        text = f"{label} {confidence:.3f}"
        plot_one_box(boxes[i], image, label=text)
    if boxes.shape[0] != 0:
        image = Image.fromarray(image)
        image_stream = io.BytesIO()
        # 将 PIL Image 对象保存到字节流中
        image.save(image_stream, format='JPEG')
        image_stream.seek(0)
        today = datetime.date.today()
        objectName =str(today) + "/" + name
        objectRes = client.put_object(resultBucketName,objectName,image_stream,length=image_stream.getbuffer().nbytes)
        tempUrl = None
        if objectRes is not None:
            tempUrl = client.presigned_get_object(resultBucketName,objectName)
        return  tempUrl
    else:
        return None
from flask import request

import requests
def getMinioPrediction(imgUrls):
    resUrls = []
    for imgUrl in imgUrls:
        response =  requests.get(imgUrl)
        name = get_last_part_of_url(imgUrl)
        if response.status_code == 200:
            fileBack =  get_prediction(response.content,name)
            resUrls.append(fileBack)
            print(fileBack)
    return resUrls
@app.route('/predict',methods = ['POST'])
def predict():
    data = request.get_json()
    images = data["uploadImages"]
    res = getMinioPrediction(images)
    return jsonify({"status":"ok", "code" : 200,"data":res})

IMAGES_PER_PAGE = 10
@app.route('/get_images/<int:page>', methods=['GET'])
def get_images(page):
    start = page * IMAGES_PER_PAGE
    end = start + IMAGES_PER_PAGE
    images = IMAGES[start:end]
    # 如果请求的页码超出范围，则返回空列表
    if not images:
        return jsonify({"error": "Page out of range"}), 404

    return jsonify({"images": images})

if __name__ == '__main__':
    app.run()

