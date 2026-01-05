
from imutils import paths
import argparse
import cv2
import os
import numpy as np
import sys

# コマンドライン引数を取得（0番目はスクリプト名）
args = sys.argv
analyzFolder = args[1]


# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--images", required=True,
#                 help="path to input directory of images")
# ap.add_argument("-t", "--threshold", type=float, default=100.0,
#                 help="focus measures that fall below this value will be considered 'blurry'")
# args = vars(ap.parse_args())

saveFolder = "C:\画像検査AI\画像検査AI"

# OpenCVのLaplacianを利用してエッジを検出する処理をするメソッドを追加

def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F)


# 検出したエッジのスコアを画像の左上に記述処理をするメソッドを追加

def report_image(image, laplacian, text):
    cv2.putText(image, "{}: {:.2f}".format(text, laplacian.var()), (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), 3)

# スコアを記述した画像を保存する処理を追加
def write_image(file_path, image):
    
    
    dir_file = os.path.split(file_path)
    dir = dir_file[0]
    
    # ディレクトリ部分を / で分割
    dir_parts = dir.split("\\")
    # ディレクトリの○○を取得
    unsouPath = dir_parts[1] +"\\"+ dir_parts[2]
    # ファイル名
    file_name = dir_file[1]
    # 保存ディレクトリ
    report_dir = saveFolder +"\\"+ unsouPath
    
    os.makedirs(report_dir, exist_ok=True)
    save_path = os.path.join(report_dir, file_name)
    # 日本語パス対応で保存
    ext = os.path.splitext(file_name)[1].lower()
    if ext in [".jpg", ".jpeg"]:
        is_success, buf = cv2.imencode(".jpg", image)
    elif ext == ".png":
        is_success, buf = cv2.imencode(".png", image)
    else:
        is_success, buf = cv2.imencode(".jpg", image)
    if is_success:
        buf.tofile(save_path)
    

# メインの処理を追加。ここでは引数のimagesで渡されたディレクトリに格納されている画像を次々に処理していきます。
# Laplacianのスコアが100以下であれば、ピンボケ写真と判断しています。

# for image_path in paths.list_images(args["images"]):C:\画像検査AI\images
for image_path in paths.list_images("G:\マイドライブ\画像"):
    # image = cv2.imread(image_path)
    
     # フォルダ名に「岡部」が含まれているか判定
    dir_name = os.path.dirname(image_path)
    if "画像" in dir_name:
        nparr = np.fromfile(image_path,np.uint8)
        
        image = cv2.imdecode(nparr,cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        laplacian = variance_of_laplacian(gray)
        
        print (laplacian.var())
        if laplacian.var() > 100:
            text = "Not Blurry"
            # if laplacian.var() < args["threshold"]:
            #     text = "Blurry"
            
            report_image(image, laplacian, text)
        
            write_image(image_path, image)
            # write_image(image_path, laplacian, "/laplacian")    
    










