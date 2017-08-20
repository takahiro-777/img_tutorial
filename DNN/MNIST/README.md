# MNIST分類問題

## 概要
```
tensorflow_tutorial for expertsのMNIST分類問題のコードを
ベースにモデルの保存と、保存したモデルを読み込んで行う推論部分に
ついて実装した。
```

## 使用方法
```
1) modelディレクトリを作成し、モデルファイルを展開する
2) コードを実行する
$ python MNIST_CNN.py
-> 推論の実行
$ python MNIST_CNN.py --run_mode train
-> 学習の実行（過去の最新のモデルを読み込んでそこから学習する）
$ python MNIST_CNN.py --run_mode train --continuity False
-> 学習の実行（過去のモデルは全て消去し、0から学習し直す）
```
