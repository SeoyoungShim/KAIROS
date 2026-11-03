
from quiz import Quiz


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.score = 0
        self.total_questions = 0

    def add_quiz(self, quiz):
        self.quizzes.append(quiz)

    def show_quizzes(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print("\n===== 퀴즈 목록 =====")

        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"{index}. {quiz.question}")

    def play(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        for quiz in self.quizzes:
            print("\n" + quiz.question)

            for index, choice in enumerate(quiz.choices, start=1):
                print(f"{index}. {choice}")

            answer = input("정답 번호를 입력하세요: ")

            if answer.isdigit() and int(answer) == quiz.answer:
                print("정답입니다!")
                self.score += 1
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

            self.total_questions += 1

    def show_score(self):
        print("\n===== 나의 점수 =====")
        print(f"맞힌 문제: {self.score}")
        print(f"푼 문제: {self.total_questions}")

        if self.total_questions > 0:
            accuracy = (self.score / self.total_questions) * 100
            print(f"정답률: {accuracy:.1f}%")
        else:
            print("아직 푼 문제가 없습니다.")

    def create_quiz(self):
        question = input("문제를 입력하세요: ").strip()

        if not question:
            print("문제는 빈칸으로 입력할 수 없습니다.")
            return

        choices = []

        for i in range(4):
            choice_text = input(f"{i + 1}번 보기를 입력하세요: ").strip()

            if not choice_text:
                print("보기는 빈칸으로 입력할 수 없습니다.")
                return

            choices.append(choice_text)

        while True:
            answer = input("정답 번호를 입력하세요 (1~4): ").strip()

            if answer in ["1", "2", "3", "4"]:
                break

            print("잘못된 입력입니다. 1~4 중에서 선택하세요.")

        quiz = Quiz(question, choices, int(answer))
        self.add_quiz(quiz)

        print("퀴즈가 추가되었습니다!")

    def run(self):
        try:
            while True:
                print("\n===== KAIROS =====")
                print("1. 퀴즈 풀기")
                print("2. 퀴즈 추가하기")
                print("3. 퀴즈 목록 보기")
                print("4. 점수 확인하기")
                print("5. 종료하기")

                choice = input("메뉴 번호를 선택하세요: ").strip()

                if choice == "1":
                    self.play()

                elif choice == "2":
                    self.create_quiz()

                elif choice == "3":
                    self.show_quizzes()

                elif choice == "4":
                    self.show_score()

                elif choice == "5":
                    print("KAIROS를 종료합니다. 감사합니다!")
                    break

                else:
                    print("잘못된 입력입니다. 1~5 중에서 선택하세요.")

        except (KeyboardInterrupt, EOFError):
            print("\nKAIROS를 안전하게 종료합니다.")
