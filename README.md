# honya

## 概要  

-高齢者の運動や，リハビリの場面において，モチベーション向上のために一緒に運動し声掛けを行うRTC群の開発を行った．  

## 特徴  

-ヒューマノイドロボットがトレーニングのガイドを行う．  
-ヒューマノイドロボットが前向きな言葉をかける．  
-立ち上がり時間の結果を表示する．  

## 仕様  

-言語：python  
-OS：Windows 10  

## コンポーネント群  

### 新規作成コンポーネント

- Judge:センサ値から人の立ち上がりを判定
- CsvWrite:csvファイルへの書き込み
- GUI:GUI表示
- Calc:立ち上がり時間の取得
- StandUp:ヒューマノイドロボットNAOへの指令  

### 既存のコンポーネント  

- SerialConnect:シリアル通信
- PortAudioInput:音声取得
- JuliusRTC:音声認識
- SEAT:対話制御

## ソースコード  

- ソースと動画とマニュアルは[]にあります
