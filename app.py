from flask import Flask, request, jsonify
from flask_cors import CORS
import base64
import requests

app = Flask(__name__)
CORS(app)

def query(prompt):
    url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(prompt)}"
    response = requests.get(url)

    print("🔍 Pollinations 응답 상태코드:", response.status_code)
    print("🔍 Content-Type:", response.headers.get("Content-Type", ""))

    if response.status_code == 200 and "image" in response.headers.get("Content-Type", ""):
        return response.content
    else:
        raise Exception(f"이미지 생성 실패: {response.text}")

@app.route("/generate", methods=["POST"])
def generate_image():
    try:
        data = request.get_json()
        prompt = data.get("prompt")

        if not prompt:
            return jsonify({"error": "📛 프롬프트가 없습니다."}), 400

        image_bytes = query(prompt)
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        image_url = f"data:image/png;base64,{image_base64}"

        return jsonify({"result": image_url})

    except Exception as e:
        print("❌ Flask 서버 처리 실패:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
