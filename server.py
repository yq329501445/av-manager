from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import sqlite3
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

def get_db():
    db = sqlite3.connect('data/video_database.db')
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT NOT NULL,
            title TEXT NOT NULL,
            actress TEXT,
            tags TEXT,
            magnet TEXT,
            rating INTEGER,
            note TEXT,
            image_path TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    db.commit()

@app.route('/')
def index():
    return render_template('index.html')

# API路由 - 获取所有记录
@app.route('/api/videos')
def get_videos():
    db = get_db()
    videos = db.execute('SELECT * FROM videos ORDER BY created_at DESC').fetchall()
    return jsonify([dict(video) for video in videos])

# API路由 - 添加新记录
@app.route('/api/videos', methods=['POST'])
def add_video():
    if 'image' not in request.files:
        return jsonify({'status': 'error', 'message': '没有上传图片'})

    file = request.files['image']
    if file.filename == '':
        image_path = None
    else:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_path = filename

    db = get_db()
    db.execute(
        'INSERT INTO videos (video_id, title, actress, tags, magnet, rating, note, image_path) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (request.form['video_id'], request.form['title'], request.form['actress'],
         request.form['tags'], request.form['magnet'], request.form['rating'],
         request.form['note'], image_path)
    )
    db.commit()
    return jsonify({'status': 'success'})

# API路由 - 获取单条记录
@app.route('/api/videos/<int:id>')
def get_video(id):
    db = get_db()
    video = db.execute('SELECT * FROM videos WHERE id = ?', (id,)).fetchone()
    if video is None:
        return jsonify({'status': 'error', 'message': '记录不存在'})
    return jsonify(dict(video))

# API路由 - 修改记录
@app.route('/api/videos/<int:id>', methods=['PUT'])
def update_video(id):
    if 'image' not in request.files:
        return jsonify({'status': 'error', 'message': '没有上传图片'})

    file = request.files['image']
    if file.filename == '':
        image_path = None
    else:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_path = filename

    db = get_db()
    db.execute(
        'UPDATE videos SET video_id = ?, title = ?, actress = ?, tags = ?, magnet = ?, rating = ?, note = ?, image_path = ? WHERE id = ?',
        (request.form['video_id'], request.form['title'], request.form['actress'],
         request.form['tags'], request.form['magnet'], request.form['rating'],
         request.form['note'], image_path, id)
    )
    db.commit()
    return jsonify({'status': 'success'})

# API路由 - 删除记录
@app.route('/api/videos/<int:id>', methods=['DELETE'])
def delete_video(id):
    db = get_db()
    db.execute('DELETE FROM videos WHERE id = ?', (id,))
    db.commit()
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

