#-*-charset=utf-8
class TestBase:
    def __init__(self, name="솔루션 테스트"):
        self.name = name

    def getName(self):
        return self.name

    def createTestCases(self):
        return [
            ["SampleData - 1"],
            ["SampleData - 2"]
        ]

    def solution(self, params):
        print(params)