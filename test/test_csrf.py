import requests

session = requests.Session()

login_data = {
    'username': 'elliot',
    'password': '123123123',
    'otp': ''
}
r1 = session.post('http://127.0.1.1:5000/user/login', data=login_data)
print('Login status:', r1.status_code)
print('Cookies:', session.cookies)

post_data = {'text': 'Tôi bị hack bởi CSRF attack!'}
r2 = session.post('http://127.0.1.1:5000/posts/', data=post_data)
print('Post status:', r2.status_code)
print('Final URL:', r2.url)