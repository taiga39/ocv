import cv2
from fastapi import FastAPI
from pydantic import BaseModel
import base64
import numpy as np
from io import BytesIO
from PIL import Image


def base64_to_pil(img_str):
  if "base64," in img_str:
      # DARA URI の場合、data:[<mediatype>][;base64], を除く
      img_str = img_str.split(",")[1]
  img_raw = base64.b64decode(img_str)
  img = Image.open(BytesIO(img_raw))

  return img

class Item(BaseModel):
    name: str

app = FastAPI()


@app.post("/image/")
async def create_item(item: Item):
  img_base = item.name
  # img_binary = base64.b64decode(img_base)
  # img_binarystream = io.BytesIO(img_binary)
  # img_pil = Image.open(img_binarystream)   
  base64_to_pil(img_base)

  img_numpy = np.asarray(base64_to_pil(img_base))

  #numpy配列(BGR) <- numpy配列(RGBA)
  img = cv2.cvtColor(img_numpy, cv2.COLOR_RGBA2BGR) 
  # cv2.imshow('window title', img_numpy_bgr)
  # cv2.waitKey(0)
  # cv2.destroyAllWindows()

  # img = cv2.imread(img)
  # カスケード型識別器の読み込み
  cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

  # グレースケール変換(グレースケールを使用すると、高速に顔検出できるらしい)
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

  # 顔領域の探索
  face = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(30, 30))

  print(type(face))

  # 顔領域を赤色の矩形で囲む
  for (x, y, w, h) in face:
      cv2.rectangle(img, (x, y), (x + w, y+h), (0,0,200), 3)

  # 結果画像を保存
  cv2.imwrite("result.jpg",img)

  return "OK"

