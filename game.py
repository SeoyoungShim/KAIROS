import json
from pathlib import Path

from quiz import Quiz


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.score = 0
        self.total_questions = 0
        self.state_file = Path("state.json")

        self.load_data()

    # 퀴즈 추가
    def add_quiz(self, quiz):
        self.quizzes.append(quiz)

    # 퀴즈 목록 보기
    def show_quizzes(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print("\n===== 퀴즈 목록 =====")

        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"{index}. {quiz.question}")

    # 퀴즈 풀기
    def play(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        for quiz in self.quizzes:
            print("\n" + quiz.question)

            for index, choice in enumerate(quiz.choices, start=1):
                print(f"{index}. {choice}")

            while True:
                answer = input("정답 번호를 입력하세요 (1~4): ").strip()

                if answer in ["1", "2", "3", "4"]:
                    break

                print("잘못된 입력입니다. 1~4 중에서 선택하세요.")

            if int(answer) == quiz.answer:
                print("정답입니다!")
                self.score += 1
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

            self.total_questions += 1

    # 점수 확인
    def show_score(self):
        print("\n===== 나의 점수 =====")
        print(f"맞힌 문제: {self.score}")
        print(f"푼 문제: {self.total_questions}")

        if self.total_questions > 0:
            accuracy = (self.score / self.total_questions) * 100
            print(f"정답률: {accuracy:.1f}%")
        else:
            print("아직 푼 문제가 없습니다.")

    # 퀴즈 추가하기
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

    # 데이터 저장
    def save_data(self):
        data = {
            "quizzes": [
                {
                    "question": quiz.question,
                    "choices": quiz.choices,
                    "answer": quiz.answer
                }
                for quiz in self.quizzes
            ],
            "score": self.score,
            "total_questions": self.total_questions
        }

        try:
            with self.state_file.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            print("게임 데이터가 저장되었습니다.")

        except OSError:
            print("데이터 저장 중 오류가 발생했습니다.")

    # 데이터 불러오기
    def load_data(self):
        if not self.state_file.exists():
            print("저장된 데이터가 없습니다. 새 게임을 시작합니다.")
            return

        try:
            with self.state_file.open("r", encoding="utf-8") as file:
                data = json.load(file)

            quizzes = [
                Quiz(item["question"], item["choices"], item["answer"])
                for item in data["quizzes"]
            ]

            score = data["score"]
            total_questions = data["total_questions"]

            if (
                not isinstance(score, int)
                or isinstance(score, bool)
                or not isinstance(total_questions, int)
                or isinstance(total_questions, bool)
                or score < 0
                or total_questions < score
            ):
                raise ValueError("점수 데이터가 올바르지 않습니다.")

            self.quizzes = quizzes
            self.score = score
            self.total_questions = total_questions

            print("저장된 게임 데이터를 불러왔습니다.")

        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            print("저장 파일이 손상되었습니다. 새 게임을 시작합니다.")

        except OSError:
            print("데이터를 불러오는 중 오류가 발생했습니다.")

    # 게임 실행
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
                    self.save_data()
                    print("KAIROS를 종료합니다. 감사합니다!")
                    break

                else:
                    print("잘못된 입력입니다. 1~5 중에서 선택하세요.")

        except (KeyboardInterrupt, EOFError):
            print("\nKAIROS를 안전하게 종료합니다.")
            self.save_data()