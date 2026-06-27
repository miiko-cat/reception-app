# 1. Pythonの公式イメージをベースにする
FROM python:3.12-slim

# 2. コンテナ内の環境変数を設定（Pythonがログをすぐに出力するようにする設定など）
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. コンテナ内の作業ディレクトリを設定
WORKDIR /code

# 4. OSパッケージを最新化（ベースイメージ内の既知の脆弱性にセキュリティパッチを当てる）
RUN apt-get update && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 5. requirements.txtをコピーしてパッケージをインストール
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# 6. プロジェクトのソースコードをすべてコンテナにコピー
COPY . /code/

# 7. Djangoの起動コマンド（本番用のGunicornで起動）
CMD ["gunicorn", "reception_app.wsgi:application", "--bind", "0.0.0.0:8000"]