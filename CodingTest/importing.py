import importlib
from TestBase import TestBase as testbase

def createSolutions():
    solutions = []

    importArray = []
    importArray.append(importlib.import_module("TestBase").TestBase())
    importArray.append(importlib.import_module(".Q1", "kakao.2018").Quiz())
    importArray.append(importlib.import_module(".Q2", "kakao.2018").Quiz())
    importArray.append(importlib.import_module(".Q3", "kakao.2018").Quiz())
    for quiz in importArray:
        solutions.append({
            "name": quiz.getName(),
            "testcases": quiz.createTestCases(),
            "answers": quiz.createAnswers(),
            "solution": quiz.solution
        })
        
    return solutions

solutions = createSolutions()