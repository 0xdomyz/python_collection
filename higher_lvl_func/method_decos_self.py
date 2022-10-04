def check_authorization(f):
    def wrapper(*args):
        print(args[0].url)
        return f(*args)

    return wrapper


class Client(object):
    def __init__(self, url):
        self.url = url

    @check_authorization
    def get(self):
        print("get")

    def get2(self):
        print("get")


if __name__ == "__main__":

    Client("http://www.google.com").get()

    check_authorization(Client("http://www.google.com").get2)()

    @check_authorization
    def get3(self):
        return self.get2()

    c = Client("http://www.google.com")
    c.get3 = get3
    c.get3()
