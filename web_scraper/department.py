class Department(object):

    def __init__(self, dept='economics'):
        self.dept = dept.lower()
        self.headers = {'User-Agent': 'Chrome/74.0.3729.169'}
        self.url = "https://{}.gmu.edu".format(self.dept)
