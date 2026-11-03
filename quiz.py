class Quiz:
    def __init__(self, question, choices, answer):
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제는 빈칸으로 입력할 수 없습니다.")

        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지는 반드시 4개여야 합니다.")

        for choice in choices:
            if not isinstance(choice, str) or not choice.strip():
                raise ValueError("선택지는 빈칸으로 입력할 수 없습니다.")

        if (
            not isinstance(answer, int)
            or isinstance(answer, bool)
            or answer not in [1, 2, 3, 4]
        ):
            raise ValueError("정답은 1부터 4까지의 숫자여야 합니다.")

        self.question = question.strip()
        self.choices = [choice.strip() for choice in choices]
        self.answer = answer

    def display(self):
        print("\n" + self.question)

        for index, choice in enumerate(self.choices, start=1):
            print(f"{index}. {choice}")

    def check_answer(self, answer):
        return answer == self.answer
