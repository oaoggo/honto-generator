from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# Flask 앱 초기화
app = Flask(__name__)

# 환경변수에서 OpenAI API 키 가져오기
openai.api_key = os.environ["OPENAI_API_KEY"]

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

def generate_dalle_image(prompt):
    response = openai.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return response.data[0].url

if __name__ == "__main__":
    app.run(debug=True)
