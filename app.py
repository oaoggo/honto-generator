from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# Flask 앱 초기화 및 CORS 설정
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

# OpenAI API 키 설정
openai.api_key = os.environ.get("OPENAI_API_KEY")

# 루트 경로: 상태 확인용
@app.route("/", methods=["GET"])
def home():
    return "✅ Honto Generator API is live!"

# 이미지 생성 요청 처리
@app.route("/generate", methods=["POST"])
def generate_content():
    data = request.get_json()
    prompt = data.get("prompt")
    content_type = data.get("type", "4cut_comic")

    if not prompt:
        return jsonify({"error": "프롬프트가 없습니다."}), 400

    try:
        if content_type == "4cut_comic":
            image_url = generate_dalle_image(prompt)
            return jsonify({"result": image_url})
        else:
            return jsonify({"error": "지원하지 않는 콘텐츠 유형입니다."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DALL·E 이미지 생성 함수
def generate_dalle_image(prompt):
    response = openai.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return response.data[0].url

# 로컬 테스트용 실행
if __name__ == "__main__":
    app.run(debug=True)
