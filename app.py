from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# OpenAI 키를 환경변수에서 가져오거나 직접 입력
openai.api_key = os.environ.get("OPENAI_API_KEY") or "여기에_당신의_API_키를_직접_입력하세요"

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
