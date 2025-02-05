import requests
import time

# بيانات تسجيل الدخول
login_data = {
    'username': '1281811280',
    'password': '123456',
    'lang': 'eg',
}

# متغير التوكن
token = None

# تهيئة الـ Headers المطلوبة
headers = {
    'authority': 'btsmoa.btswork.vip',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,ar-AE;q=0.7,ar;q=0.6',
    'content-type': 'application/x-www-form-urlencoded',
    'origin': 'https://btswork.com',
    'referer': 'https://btswork.com/',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36',
}

# بيانات السحب
withdraw_data = {
    'draw_type': 'bank',
    'user_bank_id': '65700',
    'draw_money': '4500',
    'ifsc': '',
    'fee': '450',
    'drawword': '123456',
    'walletType': '2',
    'lang': 'eg',
}

# دالة لتسجيل الدخول
def relogin():
    global token, headers
    print("🔄 إعادة تسجيل الدخول...")
    try:
        response = requests.post('https://btsmoa.btswork.vip/api/User/Login', json=login_data)
        print(f"📥 رد تسجيل الدخول: {response.text}")  # طباعة الرد كامل
        if response.status_code == 200:
            result = response.json()
            if "info" in result and "token" in result["info"]:
                token = result["info"]["token"]
                headers['Authorization'] = f'Bearer {token}'  # وضع التوكن في الهيدر
                print(f"✅ تم الحصول على التوكن الجديد: {token}")
            else:
                print("⚠️ فشل في استخراج التوكن!")
        else:
            print(f"⚠️ فشل تسجيل الدخول. الرد: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"⚠️ خطأ أثناء تسجيل الدخول: {e}")

# دالة تنفيذ السحب
def attempt_withdraw():
    global token, headers

    if not token:
        relogin()  # إذا ما في توكن، نقوم بتسجيل الدخول أولًا

    while True:
        print("💰 محاولة تنفيذ السحب...")

        try:
            # إضافة التوكن في البيانات
            withdraw_data['token'] = token

            # إرسال طلب السحب
            response = requests.post('https://btsmoa.btswork.vip/api/Transaction/draw', headers=headers, data=withdraw_data)
            print(f"📤 رد السحب: {response.text}")  # طباعة الرد كامل

            response_json = response.json()

            if response_json.get("code") == 200:
                print("✅ تمت عملية السحب بنجاح!")
                break  # الخروج بعد النجاح
            elif response_json.get("code") in [203, 204]:  # انتهاء التوكن
                print("🔄 انتهت الجلسة، إعادة تسجيل الدخول...")
                relogin()  # استرجاع توكن جديد
            else:
                print(f"⚠️ فشل السحب. الرد: {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"⚠️ خطأ أثناء إرسال الطلب: {e}")

        time.sleep(0)

# تشغيل البرنامج
attempt_withdraw()
