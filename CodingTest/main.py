import importing
import timeit

if __name__ == "__main__":
    for solution in importing.solutions:
        print()
        print()
        print("> [ {} ] Test case generating...".format(solution["name"]))
        cnt = 1
        solution["testcases"] = solution["testcases"]
        answers = solution["answers"]
        for testCase in solution["testcases"]:
            print()
            print("> Test case - %d is processing..." % cnt)
            print()
            begin = timeit.default_timer()
            result = solution["solution"](testCase)
            print("Result:", result)
            print()
            print("> [ Test case - {} ] Finished. Elapesed Time: {:f} ms".format(cnt, ((timeit.default_timer() - begin) * 1000)))
            print("> [ Test case - {} ] Answer: {}".format(cnt, answers[cnt - 1]))
            print()
            cnt += 1
        print("> [ {} ] Test case Finished.".format(solution["name"]))
