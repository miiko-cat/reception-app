# 1. Pythonの公式イメージをベースにする
FROM python:3.12-slim

# 2. コンテナ内の環境変数を設定（Pythonがログをすぐに出力するようにする設定など）
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. コンテナ内の作業ディレクトリを設定
WORKDIR /code

# 4. データベース（PostgreSQL）の接続に必要なツール等をインストール
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean

# 5. requirements.txtをコピーしてパッケージをインストール
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# 6. プロジェクトのソースコードをすべてコンテナにコピー
COPY . /code/

# 7. Djangoの起動コマンド（本番用のGunicornなどを使っても良いですが、まずは使い慣れたコマンドで）
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]