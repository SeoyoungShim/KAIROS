import json
from pathlib import Path

from quiz import Quiz


class QuizGame:
    def __init__(self):
        self.quizzes = []
        self.score = 0
        self.total_questions = 0

        self.best_score = 0.0
        self.best_correct = 0
        self.best_total = 0

        self.state_file = Path(__file__).resolve().parent / "state.json"
        self.load_data()

    # 퀴즈 추가
    def add_quiz(self, quiz):
        if not isinstance(quiz, Quiz):
            raise TypeError("Quiz 객체만 등록할 수 있습니다.")

        self.quizzes.append(quiz)

    # 퀴즈 목록 보기
    def show_quizzes(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        print("\n===== 퀴즈 목록 =====")

        for index, quiz in enumerate(self.quizzes, start=1):
            print(f"{index}. {quiz.question}")

    # 정답 번호 입력
    def get_answer(self):
        while True:
            answer = input("정답 번호를 입력하세요 (1~4): ").strip()

            if answer in ["1", "2", "3", "4"]:
                return int(answer)

            print("잘못된 입력입니다. 1~4 중에서 다시 입력하세요.")

    # 퀴즈 풀기
    def play(self):
        if not self.quizzes:
            print("등록된 퀴즈가 없습니다.")
            return

        round_correct = 0
        round_total = 0

        print("\n===== KAIROS 퀴즈 시작 =====")

        for quiz in self.quizzes:
            quiz.display()
            answer = self.get_answer()

            if quiz.check_answer(answer):
                print("정답입니다!")
                round_correct += 1
                self.score += 1
            else:
                print(f"오답입니다. 정답은 {quiz.answer}번입니다.")

            round_total += 1
            self.total_questions += 1

        round_accuracy = (round_correct / round_total) * 100

        print("\n===== 이번 게임 결과 =====")
        print(f"맞힌 문제: {round_correct}/{round_total}")
        print(f"정답률: {round_accuracy:.1f}%")

        if round_accuracy > self.best_score:
            self.best_score = round_accuracy
            self.best_correct = round_correct
            self.best_total = round_total
            print("축하합니다! 새로운 최고 점수를 달성했습니다.")

        self.save_data()

    # 점수 확인
    def show_score(self):
        print("\n===== 나의 점수 =====")

        if self.best_total > 0:
            print(
                f"최고 점수: {self.best_score:.1f}% "
                f"({self.best_correct}/{self.best_total})"
            )
        else:
            print("최고 점수: 아직 기록이 없습니다.")

        print(f"누적 정답: {self.score}")
        print(f"누적 풀이: {self.total_questions}")

        if self.total_questions > 0:
            accuracy = (self.score / self.total_questions) * 100
            print(f"누적 정답률: {accuracy:.1f}%")
        else:
            print("아직 푼 문제가 없습니다.")

    # 퀴즈 추가하기
    def create_quiz(self):
        print("\n===== 새 퀴즈 등록 =====")

        while True:
            question = input("문제를 입력하세요: ").strip()

            if question:
                break

            print("문제는 빈칸으로 입력할 수 없습니다.")

        choices = []

        for i in range(4):
            while True:
                choice_text = input(
                    f"{i + 1}번 보기를 입력하세요: "
                ).strip()

                if choice_text:
                    choices.append(choice_text)
                    break

                print("보기는 빈칸으로 입력할 수 없습니다.")

        answer = self.get_answer()

        try:
            quiz = Quiz(question, choices, answer)
            self.add_quiz(quiz)

            print("퀴즈가 추가되었습니다!")
            self.save_data()

        except (ValueError, TypeError) as error:
            print(f"퀴즈 등록 실패: {error}")

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
            "total_questions": self.total_questions,
            "best_score": self.best_score,
            "best_correct": self.best_correct,
            "best_total": self.best_total
        }

        try:
            with self.state_file.open("w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)

            print("게임 데이터가 저장되었습니다.")

        except OSError:
            print("데이터 저장 중 오류가 발생했습니다.")

    # 데이터 불러오기
    def load_data(self):
        try:
            if not self.state_file.exists():
                print("저장된 데이터가 없습니다. 새 게임을 시작합니다.")
                return

            with self.state_file.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                raise ValueError("저장 데이터 형식이 올바르지 않습니다.")

            quizzes_data = data["quizzes"]

            if not isinstance(quizzes_data, list):
                raise ValueError("퀴즈 목록 형식이 올바르지 않습니다.")

            quizzes = [
                Quiz(item["question"], item["choices"], item["answer"])
                for item in quizzes_data
            ]

            score = data["score"]
            total_questions = data["total_questions"]

            best_score = data.get("best_score", 0.0)
            best_correct = data.get("best_correct", 0)
            best_total = data.get("best_total", 0)

            if (
                not isinstance(score, int)
                or isinstance(score, bool)
                or not isinstance(total_questions, int)
                or isinstance(total_questions, bool)
                or score < 0
                or total_questions < score
            ):
                raise ValueError("누적 점수 데이터가 올바르지 않습니다.")

            if (
                not isinstance(best_score, (int, float))
                or isinstance(best_score, bool)
                or not 0 <= best_score <= 100
                or not isinstance(best_correct, int)
                or isinstance(best_correct, bool)
                or not isinstance(best_total, int)
                or isinstance(best_total, bool)
                or best_correct < 0
                or best_total < best_correct
                or (best_total == 0 and best_correct != 0)
                or (
                    best_total > 0
                    and round(best_correct / best_total * 100, 1)
                    != round(best_score, 1)
                )
            ):
                raise ValueError("최고 점수 데이터가 올바르지 않습니다.")

            self.quizzes = quizzes
            self.score = score
            self.total_questions = total_questions
            self.best_score = float(best_score)
            self.best_correct = best_correct
            self.best_total = best_total

            print("저장된 게임 데이터를 불러왔습니다.")

        except (json.JSONDecodeError, KeyError, TypeError,
                ValueError, AttributeError):
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
                    print("잘못된 입력입니다. 1~5 중에서 다시 입력하세요.")

        except (KeyboardInterrupt, EOFError):
            print("\nKAIROS를 안전하게 종료합니다.")
            self.save_data()
