## 動かし方
1. [TTSモデル動作側]/home/quarkgabber/Repositories/moe-tts/app.pyを立ち上げる
    a. やり方はそちらのREADME.mdを参照
2. [TTSモデル動作側]ngrokでTTSモデルにアクセスできるようにする
    a. やりかたはそちらのREADME.mdを参照
3. 以下のコマンドを実行
```
$ poetry install
$ poetry run python app.py https://xxxxxxx (ngrokのURL) 2> /dev/null
```