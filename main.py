from quiz import Quiz
from game import QuizGame


def create_default_quizzes():
    return [
        Quiz(
            "Python은 어떤 종류의 언어인가?",
            ["프로그래밍 언어", "운영체제", "웹 브라우저", "데이터베이스"],
            1
        ),
        Quiz(
            "Git의 주요 목적은 무엇인가?",
            ["이미지 편집", "버전 관리", "영상 재생", "문서 출력"],
            2
        ),
        Quiz(
            "GitHub는 어떤 서비스인가?",
            ["온라인 코드 저장 및 협업 플랫폼", "운영체제", "웹 브라우저", "게임 엔진"],
            1
        ),
        Quiz(
            "Docker Image는 무엇인가?",
            ["실행 중인 프로그램", "컨테이너를 만드는 설계도", "인터넷 주소", "프로그래밍 언어"],
            2
        ),
        Quiz(
            "Docker Container는 무엇인가?",
            ["이미지를 기반으로 실행되는 환경", "코드 편집기", "저장 장치", "네트워크 주소"],
            1
        )
    ]


print("================================")
print("          KAIROS")
print("     Catch the Moments.")
print("================================")
print("흘러가는 시간을 건져 올리다.")


game = QuizGame()

if not game.quizzes:
    game.quizzes = create_default_quizzes()
    print("기본 퀴즈 5개가 등록되었습니다.")

game.run()
