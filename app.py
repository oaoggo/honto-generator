from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# .env 불러오기
load_dotenv()

app = Flask(__name__)
CORS(app)

# DeepAI API 설정
DEEPAI_API_KEY = os.environ.get("DEEPAI_API_KEY")
API_URL = "https://api.deepai.org/api/text2img"

def query(prompt):
    response = requests.post(
        API_URL,
        data={"text": prompt},
        headers={"api-key": DEEPAI_API_KEY}
    )

    print("🔍 DeepAI 응답 상태코드:", response.status_code)
    print("🔍 Content-Type:", response.headers.get("Content-Type", ""))

    result = response.json()
    image_url = result.get("output_url")

    if image_url:
        return image_url
    else:
        raise Exception(f"이미지 생성 실패: {result}")

@app.route("/generate", methods=["POST"])
def generate_image():
    try:
        data = request.get_json()
        prompt = data.get("prompt")

        if not prompt:
            return jsonify({"error": "📛 프롬프트가 없습니다."}), 400

        image_url = query(prompt)
        return jsonify({"result": image_url})

    except Exception as e:
        print("❌ Flask 서버 처리 실패:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
