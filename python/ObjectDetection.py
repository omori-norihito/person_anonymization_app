#
# @brief    ObjectDetection class
#           オブジェクト検出クラス
#

import cv2
import numpy as np
from tflite_runtime.interpreter import Interpreter
import re
from typing import List, Optional, Sequence, Tuple, Union

from FileControl import FileControl
from ConstDefine import ConstDefine

from fdlite import FaceDetection, FaceDetectionModel
# from fdlite.render import Colors, detections_to_render_data, render_to_image 
from fdlite.render import Colors, detections_to_render_data, Annotation, Point, RectOrOval, FilledRectOrOval, Line
from PIL import Image
from PIL import ImageDraw
from PIL.Image import Image as PILImage


def pil2cv(image):
    ''' PIL型 -> OpenCV型 '''
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image


def cv2pil(image):
    ''' OpenCV型 -> PIL型
    https://qiita.com/derodero24/items/f22c22b22451609908ee
    '''
    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)
    return new_image


def render_to_image(
    annotations: Sequence[Annotation],
    image: PILImage,
    blend: bool = False
) -> PILImage:
    """Render annotations to an image.

    Args:
        annotations (list): List of annotations.

        image (Image): PIL Image instance to render to.

        blend (bool): If `True`, allows for alpha-blending annotations on
            top of the image.

    Returns:
        (Image) Returns the modified image.
    """
    draw = ImageDraw.Draw(image, mode='RGBA' if blend else 'RGB')
    for annotation in annotations:
        if annotation.normalized_positions:
            scaled = annotation.scaled(image.size)
        else:
            scaled = annotation
        if not len(scaled.data):
            continue
        thickness = int(scaled.thickness)
        color = scaled.color
        for item in scaled.data:
            if isinstance(item, Point):
                w = max(thickness // 2, 1)
                rc = [item.x - w, item.y - w, item.x + w, item.y + w]
                draw.rectangle(rc, fill=color.as_tuple, outline=color.as_tuple)
            elif isinstance(item, Line):
                coords = [item.x_start, item.y_start, item.x_end, item.y_end]
                draw.line(coords, fill=color.as_tuple, width=thickness)
            elif isinstance(item, RectOrOval):
                rc = [item.left, item.top, item.right, item.bottom]
                imcopy = image.copy() #もとの画像のコピーをとる
                imcut = imcopy.crop((item.left, item.top, item.right, item.bottom)) #顔の部分を切り取り
                gimg = imcut.resize([x // 8 for x in imcut.size]).resize(imcut.size) #顔の部分にモザイク処理
                image.paste(gimg, (int(item.left), int(item.top))) #もとの画像にモザイクをかけた画像をペースト
                # if item.oval:
                #     draw.ellipse(rc, outline=color.as_tuple, width=thickness)
                # else:
                #     draw.rectangle(rc, outline=color.as_tuple, width=thickness)
            elif isinstance(item, FilledRectOrOval):
                rgb = color.as_tuple
                rect, fill = item.rect, item.fill.as_tuple
                rc = [rect.left, rect.top, rect.right, rect.bottom]
                if rect.oval:
                    draw.ellipse(rc, fill=fill, outline=rgb, width=thickness)
                else:
                    draw.rectangle(rc, fill=fill, outline=rgb, width=thickness)
            else:
                # don't know how to render this
                pass
    return image

class ObjectDetection:

    # コンストラクタ
    def __init__(self):
        # mainのappPrefsオブジェクトを取得
        from __main__ import appprefs

        # 設定値をクラス変数にセット
        self.m_resolution = appprefs.m_resolution

        #画像の縦横幅を取得
        self.m_camera_width = ConstDefine.RESO_LIST[self.m_resolution][0]    #画像幅
        self.m_camera_height = ConstDefine.RESO_LIST[self.m_resolution][1]   #画像高さ

        # #0-1の範囲にあるか確認する
        # if appprefs.m_threshold >= 0 and appprefs.m_threshold <=1:
        #     self.m_threshold = appprefs.m_threshold       #信頼度の閾値

        # else:
        #     #デフォルト値を採用する
        #     self.m_threshold = ConstDefine.DEFAULT_THRESHOLD

        # print("[DEBUG]initObjectDetection m_resolution:%d" % self.m_resolution)
        # print("[DEBUG]initObjectDetection m_threshold:%f" % self.m_threshold)

        # #ラベルファイル読込
        # self.m_labels = self.load_labels(ConstDefine.LABEL_LIST_FILE)

        # #インタプリタの生成
        # #TensorFlow Liteモデル(.tfile)読込
        # self.m_interpreter = Interpreter(model_path=ConstDefine.TFLITE_FILE)
        # #メモリ確保
        # self.m_interpreter.allocate_tensors()
        # #学習モデルの入力層・出力層のプロパティ取得
        # self.m_input_details = self.m_interpreter.get_input_details()
        # self.m_output_details = self.m_interpreter.get_output_details()

        # self.cascade = cv2.CascadeClassifier(ConstDefine.CASCADE_FILE)

    #
    # @brief    Detect Object function
    #           オブジェクト検出実行関数
    # @param img        [in] memoryview    画像データ
    #
    def detect_object(self, img):

        # #検出に有効な画像サイズを取得
        # _, height, width, _ = self.m_interpreter.get_input_details()[0]['shape']

        # #サイズを変更
        # image = cv2.resize(img, (height, width))

        # #BGR -> RGB
        # image = image[:, :, [2,1,0]]

        # #次元を増やす
        # image = np.expand_dims(image, axis=0)

        #オブジェクト検出
        # results = self.detect_objects(self.m_interpreter, image, self.m_threshold)
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # face = self.cascade.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=3, minSize=(20, 20))
        pilimg = cv2pil(img)
        detect_faces = FaceDetection(model_type=FaceDetectionModel.FULL)
        faces = detect_faces(pilimg)
        if not len(faces):
            print('no faces detected')
        else:
            render_data = detections_to_render_data(faces, bounds_color=Colors.GREEN)
            print(render_data)
            img = pil2cv(render_to_image(render_data, pilimg))
        # # 顔領域を赤色の矩形で囲む
        # for (x, y, w, h) in face:
        #     x = max(0, x)
        #     y = max(0, y)
        #     x2 = min(width, x + w)
        #     y2 = min(height, y + h)
        #     cv2.rectangle(img, (x, y), (x2, y2), (0, 0, 300), 4)

        # cv2.rectangle(img, (50, 80), (125, 130), (0, 255, 0), thickness=-1)

        # if len(results) > 0:
        #     #JSON形式に変換する
        #     json_data = self.create_json_format(results)

        #     # ファイル操作オブジェクト
        #     filecontrol = FileControl()
        #     # JSONファイル保存
        #     filecontrol.save_file(json_data, ConstDefine.JSON_FILE_PATH)

        #     # httpIFオブジェクトimport
        #     from __main__ import httpif

        #     #クラウド保存するか
        #     if httpif.get_cloud_send_flag() :
        #         #クラウドへ送信する
        #         httpif.put(json_data)

        # else:
        #     pass
        return img




    # #
    # # @brief    create result by JSON format function
    # #           オブジェクト検出結果のJSON形式データ作成関数
    # # @param results                  [in] list   検出結果リスト
    # # @return                              str    JSON形式データ
    # def create_json_format(self, results):

    #     #検出数を取得（閾値以上）
    #     object_num = len(results)

    #     #JSONデータ文字列
    #     json_string ='{'\
    #                     '"objectNum":%d,'\
    #                     '"object":['\
    #                     % (object_num)

    #     #オブジェクト数ぶん繰り返し(iはカウントアップ変数)
    #     for i, result in enumerate(results, 0):
    #         name = self.m_labels[result["class_id"]+1]
    #         top, left, bottom, right = result["bounding_box"]

    #         basex = left * self.m_camera_width                  #矩形左上x座標
    #         basey = top * self.m_camera_height                  #矩形左上y座標
    #         width = (right * self.m_camera_width) - basex       #矩形幅
    #         height = (bottom * self.m_camera_height) - basey    #矩形高さ

    #         score = result["score"]

    #         json_string += '{'\
    #                         '"name":"%s",'\
    #                         '"square":'\
    #                         '{'\
    #                             '"baseX":%d,'\
    #                             '"baseY":%d,'\
    #                             '"width":%d,'\
    #                             '"height":%d},'\
    #                         '"score":%.2f'\
    #                         '}'\
    #                             % (name, basex, basey, width, height, score)

    #         #もし最後のデータでなければコロンを追記
    #         if i+1 < object_num:
    #             json_string += ','

    #     #末尾を追記
    #     json_string += ']}'

    #     return json_string

    # #
    # # @brief    load label file function
    # #           ラベルファイル読込関数
    # # @param path                [in] string   ラベルファイルパス
    # # @return                        list      ラベルリスト
    # def load_labels(self, path):
    #     #ファイルオープン
    #     with open(path, 'r', encoding='utf-8') as f:
    #         #ファイル内容を全部読み出す
    #         lines = f.readlines()
    #         labels = {}
    #         #行番号 ラベル名
    #         for row_number, content in enumerate(lines):
    #             #ファイル内の形式が、数字とラベル名のペアであった場合を考慮する
    #             #ラベル名の改行文字を削除し空白文字部分で分割してリストで保持
    #             pair = re.split(r'[:\s]+', content.strip(), maxsplit=1)

    #             #リストの先頭に数字がある場合
    #             if len(pair) == 2 and pair[0].strip().isdigit():
    #                 #リストに記載されていた番号とラベル名を対応させる
    #                 labels[int(pair[0])] = pair[1].strip()

    #             else:
    #                 #行番号とラベル名を対応させる
    #                 labels[row_number] = pair[0].strip()

    #     return labels

    # #
    # # @brief    set tensor input function
    # #           テンサーフローへの入力関数
    # # @param interpreter          [in] Interpreter   インタプリタ
    # # @param image                [in] list           画像データ
    # def set_input_tensor(self, interpreter, image):
    #     #入力index取得
    #     tensor_index = interpreter.get_input_details()[0]['index']
    #     #入力部取得
    #     input_tensor = interpreter.tensor(tensor_index)()[0]
    #     #入力
    #     input_tensor[:, :] = image


    # # @brief    get tensor output function
    # #           テンサーフローからの出力関数
    # # @param interpreter          [in] Interpreter   インタプリタ
    # # @param index                [in] int           インデックス番号
    # # @return                        list            出力結果
    # def get_output_tensor(self, interpreter, index):
    #     output_details = interpreter.get_output_details()[index]
    #     tensor = np.squeeze(interpreter.get_tensor(output_details['index']))
    #     return tensor




    # # @brief    detect objects function
    # #           オブジェクト検出関数
    # # @param interpreter          [in] Interpreter   インタプリタ
    # # @param image                [in] list          画像データ
    # # @param threshold            [in] int           信用度閾値
    # # @return                        list            出力結果
    # def detect_objects(self, interpreter, image, threshold):
    #     self.set_input_tensor(interpreter, image)
    #     interpreter.invoke()

    #     #出力詳細取得
    #     boxes = self.get_output_tensor(interpreter, 0)      # 比率(Top, Left, Bottom, Right)
    #     classes = self.get_output_tensor(interpreter, 1)    # クラス
    #     scores = self.get_output_tensor(interpreter, 2)     # 信用度 (0.0-1.0)
    #     count = int(self.get_output_tensor(interpreter, 3)) # 検出数

    #     results = []        #返却用リスト

    #     #検出数だけ繰り返し
    #     for i in range(count):
    #         #閾値チェック
    #         if scores[i] >= threshold:
    #             #オブジェクト毎に辞書を作成
    #             result = {
    #                 'bounding_box': boxes[i],
    #                 'class_id': classes[i],
    #                 'score': scores[i]
    #             }

    #             #辞書をリストに追加
    #             results.append(result)

    #     return results


