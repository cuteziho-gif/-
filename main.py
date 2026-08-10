import os
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.text import LabelBase
from kivy.storage.jsonstore import JsonStore

# ----------------------------------------------------
# 1. 안드로이드 한글 폰트 자동 검색 및 등록
# ----------------------------------------------------
def register_korean_font():
    # 안드로이드 기기에서 흔히 사용하는 한글 폰트 경로 리스트
    font_paths = [
        "/system/fonts/NotoSansCJK-Regular.ttc",
        "/system/fonts/NotoSansKR-Regular.otf",
        "/system/fonts/NanumGothic.ttf",
        "/system/fonts/DroidSansFallback.ttf"
    ]
    
    selected_font = None
    for path in font_paths:
        if os.path.exists(path):
            selected_font = path
            break
            
    if selected_font:
        # Kivy 기본 폰트를 한글 지원 폰트로 교체
        LabelBase.register(name="Roboto", fn_regular=selected_font)
        print(f"한글 폰트 적용 완료: {selected_font}")
    else:
        print("경고: 안드로이드 한글 폰트 경로를 찾지 못했습니다. 동일 폴더에 NanumGothic.ttf 등을 배치해주세요.")

# 앱 시작 전 폰트 등록 함수 실행
register_korean_font()


# ----------------------------------------------------
# 2. 메인 타자게임 레이아웃
# ----------------------------------------------------
WORDS = ["파이썬", "파이드로이드", "키비", "유지호", "모바일앱", "타자게임", "프로그래밍", "스마트폰", "자바스크립트", "알고리즘"]

class TypingGame(BoxLayout):
    def __init__(self, **kwargs):
        super(TypingGame, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15

        # 데이터 저장소 초기화 (scores.json 파일 생성)
        self.store = JsonStore('scores.json')
        self.high_score = self.load_high_score()

        # 게임 상태 변수
        self.score = 0
        self.time_left = 30
        self.current_word = ""
        self.timer_event = None

        # 1. 타이틀 레이블
        self.title_label = Label(
            text="[ 유지호의 타자게임 ]", 
            font_size='26sp', 
            size_hint_y=0.12
        )
        self.add_widget(self.title_label)

        # 2. 상태 표시 (현재 점수 / 최고 점수 / 남은 시간)
        self.status_label = Label(
            text=f"점수: 0 | 최고점수: {self.high_score} | 시간: 30초", 
            font_size='16sp', 
            size_hint_y=0.1
        )
        self.add_widget(self.status_label)

        # 3. 제시어 레이블
        self.word_label = Label(
            text="'게임 시작' 버튼을 누르세요!", 
            font_size='30sp', 
            size_hint_y=0.28
        )
        self.add_widget(self.word_label)

        # 4. 입력 창
        self.input_field = TextInput(
            multiline=False, 
            font_size='22sp', 
            size_hint_y=0.2,
            disabled=True
        )
        self.input_field.bind(on_text_validate=self.check_answer)
        self.add_widget(self.input_field)

        # 5. 시작 버튼
        self.start_btn = Button(
            text="게임 시작", 
            font_size='20sp', 
            size_hint_y=0.15
        )
        self.start_btn.bind(on_press=self.start_game)
        self.add_widget(self.start_btn)

    def load_high_score(self):
        """저장소에서 최고 점수 불러오기"""
        if self.store.exists('user_data'):
            return self.store.get('user_data').get('high_score', 0)
        return 0

    def save_high_score(self, new_score):
        """저장소에 최고 점수 기록하기"""
        self.store.put('user_data', high_score=new_score)

    def start_game(self, instance):
        """게임 초기화 및 타이머 시작"""
        self.score = 0
        self.time_left = 30
        self.input_field.disabled = False
        self.input_field.text = ""
        self.input_field.focus = True
        self.start_btn.disabled = True
        
        self.update_status()
        self.next_word()

        if self.timer_event:
            Clock.unschedule(self.timer_event)
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def next_word(self):
        """무작위 제시어 선택"""
        self.current_word = random.choice(WORDS)
        self.word_label.text = self.current_word

    def check_answer(self, instance):
        """정답 확인 및 점수 계산"""
        if not self.input_field.disabled:
            user_input = self.input_field.text.strip()
            if user_input == self.current_word:
                self.score += 10
                
                # 최고 점수 즉시 갱신 반영
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score(self.high_score)
                
                self.update_status()
                self.input_field.text = ""
                self.next_word()
            else:
                self.input_field.text = ""

    def update_timer(self, dt):
        """타이머 차감"""
        self.time_left -= 1
        self.update_status()
        
        if self.time_left <= 0:
            Clock.unschedule(self.timer_event)
            self.game_over()

    def update_status(self):
        """화면 상단 점수판 갱신"""
        self.status_label.text = f"점수: {self.score} | 최고점수: {self.high_score} | 시간: {self.time_left}초"

    def game_over(self):
        """게임 종료 처리"""
        msg = f"게임 종료!\n최종 점수: {self.score}점"
        if self.score >= self.high_score and self.score > 0:
            msg += "\n🎉 축하합니다! 최고 기록 달성!"
        
        self.word_label.text = msg
        self.input_field.disabled = True
        self.start_btn.disabled = False


class JihoTypingApp(App):
    def build(self):
        return TypingGame()

if __name__ == '__main__':
    JihoTypingApp().run()