from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
import base64

app = Flask(__name__)
CORS(app)

# Hugging Face API 설정
HUGGINGFACE_API_TOKEN = os.environ.get("HUGGINGFACE_API_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/prompthero/openjourney"

headers = {
    "Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"
}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)

    content_type = response.headers.get("Content-Type", "")
    if "image" in content_type:
        return response.content
    else:
        print("❌ 이미지가 아닌 응답:", response.text)
        raise Exception(f"이미지 생성 실패: {response.text}")

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
