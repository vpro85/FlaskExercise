try:
    import unittest
    from main import app
except Exception as e:
    print("Some modules are missing: {}".format(e))


class TestMain(unittest.TestCase):
    def test_repo(self):
        tester = app.test_client(self)
        response = tester.get("/vpro85/jwt-auth")
        status_code = response.status_code
        self.assertEqual(status_code, 200)

    def test_repo_content(self):
        tester = app.test_client(self)
        response = tester.get("/vpro85/jwt-auth")
        self.assertEqual(response.content_type, "application/json")

    def test_repo_check_id(self):
        tester = app.test_client(self)
        response = tester.get("/vpro85/jwt-auth")
        self.assertTrue(b'79230367' in response.data)


if __name__ == "__main__":
    unittest.main()
