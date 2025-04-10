from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import time
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

app = Flask(__name__)
CORS(app)

# Replicate API 토큰
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
        # 1단계: 이미지 생성 요청
        url = "https://api.replicate.com/v1/predictions"
        headers = {
            "Authorization": f"Token {REPLICATE_API_TOKEN}",
            "Content-Type": "application/json"
        }
        body = {
            "version": "db21e45e16f8f0bb0a8c8d3e50d68f09058f1cb14dbb36f3ccf1bdf8b5fb115b",  # SDXL 1.0 버전
            "input": {
                "prompt": prompt,
                "width": 512,
                "height": 512,
                "num_inference_steps": 30,
                "guidance_scale": 7.5
            }
        }

        response = requests.post(url, headers=headers, json=body)
        prediction = response.json()

        prediction_id = prediction.get("id")
        if not prediction_id:
            return jsonify({"error": prediction.get("detail", "예측 요청 실패")}), 500

        # 2단계: 결과 polling
        status_url = f"https://api.replicate.com/v1/predictions/{prediction_id}"
        for _ in range(20):  # 최대 20초 대기
            result_res = requests.get(status_url, headers=headers)
            result_data = result_res.json()

            if result_data["status"] == "succeeded":
                image_url = result_data["output"][0]
                return jsonify({"result": image_url})
            elif result_data["status"] == "failed":
                return jsonify({"error": "이미지 생성 실패"}), 500
            time.sleep(1)

        return jsonify({"error": "시간 초과로 이미지 생성 실패"}), 504

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# 로컬 개발용
if __name__ == "__main__":
    app.run(debug=True)
