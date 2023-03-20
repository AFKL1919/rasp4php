import unittest
import requests as r

class TestController(unittest.TestCase):

    sess = r.session()

    def test_1_login(self):
        data = {
            'username': 'rasp_admin',
            'password': '123123',
        }
        res = self.sess.post('http://127.0.0.1:9999/api/user/login', data=data)

        print(res.json())
        print(res.cookies.get("session"))
    
    def test_2_alarm_log(self):
        res = self.sess.get("http://127.0.0.1:9999/api/log/alarm")
        try:
            print(res.json())
        except:
            print(res.text)
        

if __name__ == '__main__':
    unittest.main()