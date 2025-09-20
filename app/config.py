import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL")
