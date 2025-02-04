from flask import Flask, request
import redis
import os

app = Flask(__name__)

## Configure Redis connection (environment variables are best for production)
redis_host = os.environ.get("REDIS_HOST", "127.0.0.1")  # Default to localhost
redis_port = int(os.environ.get("REDIS_PORT", 6379))  # Default to 6379
redis_password = os.environ.get("REDIS_PASSWORD") # Optional password

try:
    r = redis.Redis(host=redis_host, port=redis_port, password=redis_password, decode_responses=True)
    r.ping()  # Check connection
    print("Connected to Redis")
except redis.exceptions.ConnectionError as e:
    print(f"Redis connection error: {e}")
    exit(1)  # Exit if Redis is not available

@app.route('/', methods=['GET'])
def index():
    try:
        page_url = '/'  # Or use request.path for different URLs
        count = r.incr("pycounters")  # Atomically increment and get count
        return f"<h1 style='color: blue'>You are the {count}th visitor</h1>"
    except redis.exceptions.RedisError as e:
        print(f"Redis error: {e}")
        return "Error tracking visits.", 500  # Internal Server Error

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)  # host='0.0.0.0' for external access (dev only)