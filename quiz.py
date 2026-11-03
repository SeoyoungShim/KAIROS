class Quiz:
    def __init__(self, question, choices, answer):

        # 문제 검증
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제는 빈칸으로 입력할 수 없습니다.")

        # 선택지 개수 검증
        if not isinstance(choices, list) or len(choices) != 4:
            raise ValueError("선택지는 반드시 4개여야 합니다.")

        # 선택지 내용 검증
        for choice in choices:
            if not isinstance(choice, str) or not choice.strip():
                raise ValueError("선택지는 빈칸으로 입력할 수 없습니다.")

        # 정답 번호 검증
        if (
            not isinstance(answer, int)
            or isinstance(answer, bool)
            or answer not in [1, 2, 3, 4]
        ):
            raise ValueError("정답은 1부터 4까지의 숫자여야 합니다.")

        self.question = question.strip()
        self.choices = [choice.strip() for choice in choices]
        self.answer = answer