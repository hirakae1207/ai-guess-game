# AI推理ゲーム

マジカルバナナのアレンジ版。似たような2種類のお題となるキーワードが出される。
お題は1人だけ別のお題となっており、ユーザーはお題のキーワードをAIに渡す。
AIがどちらのお題に近いか判定して遊ぶパーティーゲーム。

### ゲームのルール
#### １ラウンドの流れ
- テーマ選択
- ニックネーム入力
- ４人分
	- ニックネーム表示
	- お題提示（ランダム）
	- キーワード入力
- AI判定
- 結果
#### 勝敗条件
- ラウンドは１ラウンド
- 勝敗条件はAIが判定し、当たったほうが勝ち
- キーワードから一番推測できる確率が高いものをAIは判定結果とする

### 技術構成
- フロント
	- HTML/CSS
- バックエンド
	- python
	- my sql
- AI判定API
	- Google gemini apiを使用

## 起動方法

### 前提条件
- Docker Desktop がインストールされていること

### 手順

1. リポジトリをクローン
```bash
   git clone https://github.com/hirakae1207/ai-guess-game.git
   cd ai-guess-game
```

2. `.env`ファイルを作成し、以下の環境変数を設定
- DB_ROOT_PASSWORD=任意のパスワード
- DB_NAME=任意のDB名

3. コンテナをビルドして起動
```bash
   docker compose up --build
```

4. ブラウザで以下にアクセス
http://localhost:8000/static/index.html

### 停止方法
```bash
docker compose down
```