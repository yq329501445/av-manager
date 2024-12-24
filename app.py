from flask import Flask, render_template, request, jsonify
import sqlite3
from datetime import datetime
import os
from pathlib import Path

app = Flask(__name__)

# 获取当前文件所在目录
BASE_DIR = Path(__file__).resolve().parent

# 修改数据库路径
DATABASE = os.path.join(BASE_DIR, 'data', 'av_database.db')

# 修改上传目录
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')

# 确保目录存在
os.makedirs(os.path.join(BASE_DIR, 'data'), exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 数据库连接
def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

# 初始化数据库
def init_db():
    db = get_db()
    db.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        av_id TEXT UNIQUE,
        title TEXT,
        actress TEXT,
        tags TEXT,
        magnet TEXT,
        note TEXT,
        rating INTEGER,
        image_path TEXT,
        created_at TEXT
    )
    ''')
    db.commit()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

