# person_anonymization_app

Vieureka用人物匿名化アプリ

## 概要

本アプリはカメラ画角に写った人物の匿名化を行い、その結果をプレビューする機能を搭載しています。
オブジェクトの検出には Tensor Flow Lite のモデルを使用しています。
プレビューではカメラ画像の人物にモザイクを描画したものを表示します。

## 機器構成

本アプリを動作させる際の機器構成を以下に示します。

- VRK-C301
- PC: ブラウザ上でリアルタイムに確認できます。

## 動作環境

- VRK-C301
    - Firmware Version : 0.86-20201013-ae5f8fec0
    - Adam Version : 1-1-1-010038
- PC
    - OS : Windows 10
    - ブラウザ : Google Chrome

## 利用したライブラリ

- VRK-C301
    - [Face Detection For Python](https://github.com/patlevin/face-detection-tflite)


## 注意事項

デモの開始・停止や画像の表示・非表示を頻繁に繰り返すと動作が不安定になる可能性があります。

動作が不安定になった場合はカメラにアクセスして UI 画面からアプリの停止、起動を実施してください。


## アプリケーションインストール方法

アプリケーションのインストール方法については、「Vieureka カメラ操作マニュアル」を参照して
「pyPersonAnonymizationApp_V1_0_vrkc301.ext」のファイルをインストールしてください

## 使い方（UI 画面）

1.カメラにアクセスして UI からアプリを起動します。
アプリ名は「Person Anonymization Application by Python」です。

Start を押下すると、画像の撮影とオブジェクト検出を開始します。

2.InstallID を元に UI 画面にログインします。
URL の<install_id>は ApplicationList に表示された値に置き換えてください。

```
http://<camaera_address>/cgi-bin/adam.cgi?methodName=sendDataToAdamApplication&installId=<install_id>&s_appDataType=0&s_appData=
```


アドレス、InstallID が正しければ以下の画面を表示します。デフォルトの動作は以下になります。

- 更新間隔：250ms
- 表示画角：VGA(640x480)

3.各機能の紹介を以下に記載します。
① インストール ID
アプリのインストール ID を表示します。

② 表示更新間隔
表示の更新間隔を変更出来ます。
変更後に Start ボタンを押下して更新間隔の変更を反映します。

注釈
ブラウザ側 Javascript の更新間隔を変更するだけですので、カメラ側の
Framerate を変更しているわけではありません。

③ デモ動作制御
Start でデモが開始します。Stop でデモが停止します。

④ 検出結果表示エリア
人物匿名化の結果を表示するエリアです。
人物検出した位置をモザイクで描画します。

