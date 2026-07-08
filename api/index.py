from flask import Flask, request, jsonify, Response
import requests

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, Proxy Server is running!'

# مسار لمحاكاة طلب settings
@app.route('/proxy/settings', methods=['POST'])
def proxy_settings():
    # استقبال البيانات من المستخدم
    data = request.get_json()
    if not data or 'space_domain' not in data or 'payload' not in data:
        return jsonify({"error": "Missing 'space_domain' or 'payload' in request"}), 400

    space_domain = data['space_domain']
    payload = data['payload']

    try:
        print(f"   -> Sending payload to {space_domain}")
        # إرسال الطلب الفعلي
        response = requests.post(f"{space_domain}/settings", json=payload, timeout=15)
        
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        # إرجاع نفس الاستجابة ونفس كود الحالة للمستخدم
        return Response(
            response.content, 
            status=response.status_code, 
            content_type=response.headers.get('Content-Type', 'text/plain')
        )

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to send settings to {space_domain}: {e}")
        return jsonify({"error": str(e)}), 500


# مسار لمحاكاة طلب start
@app.route('/proxy/start', methods=['POST'])
def proxy_start():
    # استقبال البيانات من المستخدم
    data = request.get_json()
    if not data or 'space_domain' not in data:
        return jsonify({"error": "Missing 'space_domain' in request"}), 400

    space_domain = data['space_domain']

    try:
        print(f"▶️ Sending START command to {space_domain}")
        # إرسال الطلب الفعلي
        response = requests.get(f"{space_domain}/start", timeout=15)
        
        print(f"✅ Status: {response.status_code}")
        print(f"📄 Response: {response.text}")
        
        # إرجاع نفس الاستجابة ونفس كود الحالة للمستخدم
        return Response(
            response.content, 
            status=response.status_code, 
            content_type=response.headers.get('Content-Type', 'text/plain')
        )

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to send START to {space_domain}: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
