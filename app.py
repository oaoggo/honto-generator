import os
import base64
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

app = Flask(__name__)
CORS(app)  # 프론트엔드(honto.html)에서 호출 허용

# Hugging Face API 설정
HUGGINGFACE_API_TOKEN = os.environ.get("HUGGINGFACE_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/prompthero/openjourney"
headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
}

# 이미지 생성 요청 함수
def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.content

@app.route("/generate", methods=["POST"])
def generate_image():
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "프롬프트가 없습니다."}), 400

    try:
        image_bytes = query({"inputs": prompt})
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        image_url = f"data:image/png;base64,{image_base64}"
        return jsonify({"result": image_url})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
