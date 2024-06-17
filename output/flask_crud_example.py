from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_uri'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    content = db.Column(db.Text, nullable=False)

@app.route('/posts', methods=['POST'])
def create_post():
    post = Post(title=request.json['title'], content=request.json['content'])
    db.session.add(post)
    db.session.commit()
    return jsonify({'message': 'Post created'})

@app.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.all()
    return jsonify([{'id': post.id, 'title': post.title, 'content': post.content} for post in posts])

@app.route('/posts/<int:post\_id>', methods=['GET'])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify({"id": post.id, "title": post.title, "content": post.content})

@app.route('/posts/<int:post\_id>', methods=['PUT'])
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    post.title = request.json['title']
    post.content = request.json['content']
    db.session.commit()
    return jsonify({"message": "Post updated"})

@app.route('/posts/<int:post\_id>', methods=['DELETE'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted"})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)