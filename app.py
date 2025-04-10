from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import time
from dotenv import load_dotenv

# .env 파일 로드
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
        # Step 1. Replicate에 이미지 생성 요청
        url = "https://api.replicate.com/v1/predictions"
        headers = {
            "Authorization": f"Token {REPLICATE_API_TOKEN}",
            "Content-Type": "application/json"
        }
        body = {
            "version": "db21e45e16f8f0bb0a8c8d3e50d68f09058f1cb14dbb36f3ccf1bdf8b5fb115b",  # SDXL 1.0
            "input": {
                "prompt": prompt,
                "width": 512,
                "height": 512,
                "num_inference_steps": 30,
                "guidance_scale": 7.5
            }
        }

        response = requests.post(url, headers=headers, json=body)

        # Step 2. 응답 본문이 비어 있거나 JSON이 아닌 경우 방어
        if not response.text or not response.text.strip().startswith('{'):
            return jsonify({"error": f"Replicate 응답이 비어있거나 JSON이 아님", "raw": response.text}), 500

        try:
            prediction = response.json()
        except Exception as e:
            return jsonify({"error": f"JSON 파싱 실패: {str(e)}", "raw": response.text}), 500

        prediction_id = prediction.get("id")
        if not prediction_id:
            return jsonify({"error": prediction.get("detail", "prediction ID 없음")}), 500

        # Step 3. Polling - 이미지 생성 완료 대기
        status_url = f"https://api.replicate.com/v1/predictions/{prediction_id}"
        for _ in range(20):  # 최대 20초 기다림
            result_res = requests.get(status_url, headers=headers)
            result_data = result_res.json()

            if result_data["status"] == "succeeded":
                image_url = result_data["output"][0]
                return jsonify({"result": image_url})
            elif result_data["status"] == "failed":
                return jsonify({"error": "Stable Diffusion 이미지 생성 실패"}), 500

            time.sleep(1)

        return jsonify({"error": "⏰ 이미지 생성 시간 초과"}), 504

    except Exception as e:
        return jsonify({"error": f"서버 처리 중 예외 발생: {str(e)}"}), 500

# 로컬 실행용
if __name__ == "__main__":
    app.run(debug=True)
