from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")

@app.route("/", methods=["GET"])
def home():
    return "✅ Stable Diffusion Generator API is live!"

@app.route("/generate", methods=["POST"])
def generate_image():
    data = request.get_json()
    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "프롬프트가 없습니다."}), 400

    try:
        url = "https://api.replicate.com/v1/predictions"
        headers = {
            "Authorization": f"Token {REPLICATE_API_TOKEN}",
            "Content-Type": "application/json"
        }
        body = {
            "version": "db21e45e16f8f0bb0a8c8d3e50d68f09058f1cb14dbb36f3ccf1bdf8b5fb115b",
            "input": {
                "prompt": prompt,
                "width": 512,
                "height": 512,
                "num_inference_steps": 30,
                "guidance_scale": 7.5
            }
        }

        res = requests.post(url, headers=headers, json=body)
        output = res.json()

        # Replicate의 응답 구조 체크
        if "urls" in output and output["urls"].get("get"):
            # 응답 URL에서 실제 이미지 생성 완료 여부 확인
            prediction_url = output["urls"]["get"]
            for _ in range(30):  # 최대 30초 대기
                poll_res = requests.get(prediction_url, headers=headers)
                poll_output = poll_res.json()
                if poll_output.get("status") == "succeeded":
                    return jsonify({"result": poll_output["output"][0]})
                elif poll_output.get("status") == "failed":
                    return jsonify({"error": "이미지 생성 실패"}), 500
                time.sleep(1)

            return jsonify({"error": "시간 초과로 이미지 생성 실패"}), 504

        return jsonify({"error": "예상치 못한 응답"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
