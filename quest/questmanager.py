
class QuestManager:
    def __init__(self):
        self.quest_list=[Q1(),Q2()]
        self.current_index=0
        # intro → progress → complete

    def get_current_dialogue(self):
        """현재 진행 중인 퀘스트의 대사 목록을 반환"""
        current_quest = self.quest_list[self.current_index]
        return current_quest.dialogues[current_quest.state]
    def on_dialogue_end(self):
        """
        대사가 끝났을 때 어떤 상태로 넘어갈지 관리
        """
        if self.current_quest == "q1" and self.quest_state == "intro":
            self.quest_state = "progress"

        elif self.current_quest == "q1" and self.quest_state == "progress":
            # 예: 퀘스트 목표를 달성하면 외부에서 complete로 바꿔줄 수도 있음
            pass

        elif self.current_quest == "q1" and self.quest_state == "complete":
            self.current_quest = "q2"
            self.quest_state = "intro"

    def check_progress(self, target_type):
        current_quest = self.quest_list[self.current_index]
        current_quest.check_progress(target_type)
        # 이후 q3, q4 도 이런 식으로 확장 가능
def load_dialogue(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        return [line.strip() for line in lines]
class Q1:
    def __init__(self):
        self.state = "intro"
        self.dialogues = {
            "intro": [],
            "progress": [],
            "complete": [],
        }
        self.dialogues["intro"] = load_dialogue('asset/map/town/Snorlax/quest/q1.txt')
        self.dialogues["progress"] = load_dialogue('asset/map/town/Snorlax/quest/process.txt')
        self.dialogues["complete"] = load_dialogue('asset/map/town/Snorlax/quest/q1_complete.txt')
        # intro → progress → complete
        self.target=5
        self.target_type = 1
        self.current=0
        self.pt="연구원 처치 진행도: "
        self.step=0
    def update_state(self, new_state):
        self.state = new_state
    def check_progress(self,target_type):
        if self.target_type==target_type:
            self.current+=1
            print(self.current)
            if self.current>=self.target:
                self.state="complete"


class Q2:
    def __init__(self):
        self.state = "intro"
        self.dialogues = {
            "intro": [],
            "progress": [],
            "complete": [],
        }
        self.dialogues["intro"] = load_dialogue('asset/map/town/Snorlax/quest/q2.txt')
        self.dialogues["progress"] = load_dialogue('asset/map/town/Snorlax/quest/process.txt')
        self.dialogues["complete"] = load_dialogue('asset/map/town/Snorlax/quest/q2_complete.txt')
        # intro → progress → complete
        self.target = 5
        self.target_type=4
        self.current = 0
        self.pt = "연구원 처치 진행도: "
        self.step = 0

    def update_state(self, new_state):
        self.state = new_state
    def check_progress(self,target_type):
        if self.target_type==target_type:
            self.current+=1
            if self.current>=self.target:
                self.state="complete"