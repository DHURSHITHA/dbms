from flask import Flask, jsonify
import fakeredis as redis
import ast
import time

app = Flask(__name__)
redis_client = redis.FakeStrictRedis(decode_responses=True)

def get_blog_post_from_db(post_id):
    time.sleep(2)  # Simulate database delay
    return {"post_id": post_id, "title": f"Post {post_id}", "content": "Sample blog content."}

@app.route('/')
def home():
    return "Welcome to the Blog API!"

@app.route('/post/<post_id>')
def get_post(post_id):
    cached_post = redis_client.get(post_id)
    if cached_post:
        return jsonify({"source": "cache", "data": ast.literal_eval(cached_post)})
    post = get_blog_post_from_db(post_id)
    redis_client.setex(post_id, 10, str(post))
    return jsonify({"source": "database", "data": post})

@app.route('/clear-cache/<post_id>')
def clear_cache(post_id):
    redis_client.delete(post_id)
    return jsonify({"message": f"Cache for post {post_id} cleared."})

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)   # <--- important
