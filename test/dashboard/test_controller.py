import unittest
import requests as r

class TestController(unittest.TestCase):

    sess = r.session()

    def test_1_register(self):
        data = {
            'username': 'rasp_admin',
            'password': '123123',
        }
        res = self.sess.post('http://127.0.0.1:9999/api/user/admin_register', data=data)

        print(res.json())
        print(res.cookies.get("session"))

    def test_2_get_all_rule(self):
        res = self.sess.get("http://127.0.0.1:9999/api/rules")

        print(res.json())
    
    def test_3_get_rule_with_classname(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = {
            'classname': 'DefaultUserIPFilter',
            'rule_type': 1
        }

        res = self.sess.post("http://127.0.0.1:9999/api/rule", data=data)

        print(res.json())

    def test_4_rule_update(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        data = {
            'classname': 'DefaultUserIPFilter',
            'rule_id': '1',
            'data': '172.18.0.1',
            'rule_type': '1',
        }

        res = self.sess.post('http://127.0.0.1:9999/api/rule/update', headers=headers, data=data)

        print(res.json())
    
    def test_5_install(self):
        res = self.sess.get('http://127.0.0.1:9999/api/install')

        print(res.json())
        

if __name__ == '__main__':
    unittest.main()