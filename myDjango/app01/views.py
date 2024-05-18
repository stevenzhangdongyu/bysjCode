import os.path
import subprocess
from django.http import HttpResponse
from django.shortcuts import render
import PIL.Image
import io
# Create your views here.
def index(request):
    return HttpResponse("welcome!")
def userList(request):
    return render(request,"user_list.html")

def clear_folder(folder_path):
    # 遍历文件夹中的所有文件和文件夹
    for file_name in os.listdir(folder_path):
        # 构造文件或文件夹的完整路径
        file_path = os.path.join(folder_path, file_name)
        # 如果是文件，则删除
        if os.path.isfile(file_path):
            os.remove(file_path)
        # 如果是文件夹，则递归删除文件夹内的内容
        elif os.path.isdir(file_path):
            clear_folder(file_path)
def home(request):
    if request.method == "GET":
        return render(request,"home.html")
    else:
        targetPath = 'app01/static/img/'
        file = request.FILES.get("avatar")
        fileName = file.name
        filePath = os.path.join(targetPath,fileName)
        with open(filePath,'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        process = subprocess.Popen(["D:\\anaconda3\\envs\\Yolo\\python", "E:\\PythonProject\\detr\\detr\\detect.py","--input_dir","E:\\PythonProject\\myDjango\\app01\\static\\img",
                                    "--output_dir","E:\\PythonProject\\myDjango\\app01\\static\\imgOutput"])
        process.wait()
        outPutFilePath = os.path.join('app01/static/imgOutput',fileName)
        pil_image = PIL.Image.open(outPutFilePath)

        # 创建一个字节流对象
        image_stream = io.BytesIO()

        # 将 PIL Image 对象保存到字节流中
        pil_image.save(image_stream, format='JPEG')

        # 将字节流对象转换为二进制数据
        image_binary = image_stream.getvalue()
        clear_folder('app01/static/img/')
        clear_folder('app01/static/imgOutput')
        # 返回图片给前端
        return HttpResponse(image_binary, content_type='image/jpeg')