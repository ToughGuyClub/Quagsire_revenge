import game_framework
import game_world
from pico2d import *


class QuestManager:
    def __init__(self,player):
        self.quest_list=[Q1(player),Q2(player),Q3(player),Q4(player),Q5(player)]
        self.clear_quest=0
        self.current_index=0
        self.player=player
        # intro → progress → complete

    def get_current_dialogue(self):
        """현재 진행 중인 퀘스트의 대사 목록을 반환"""
        current_quest = self.quest_list[self.current_index]
        return current_quest.dialogues[current_quest.state]

    def draw(self):
        current_quest = self.quest_list[self.current_index]
        current_quest.draw()
    def check_progress(self, target_type):
        current_quest = self.quest_list[self.current_index]
        result = current_quest.check_progress(target_type)
        if result and current_quest.state == "Realcomplete":
            self.clear_quest=result

        print("현재 클리어한 퀘스트 번호:",self.clear_quest)

    def change_step(self,new_step):
        self.quest_list[self.current_index].step=new_step

    def draw(self):
        current_quest = self.quest_list[self.current_index]
        current_quest.draw()
def load_dialogue(path):
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        return [line.strip() for line in lines]
class Q1:
    def __init__(self,player):
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
        self.player=player
        #누오 잠만보 이미지
        self.s_Nimg = load_image(os.path.join('asset/map/town/Snorlax', 'Normal.png'))
        self.s_Cimg = load_image(os.path.join('asset/map/town/Snorlax', 'Crying.png'))
        self.s_Iimg = load_image(os.path.join('asset/map/town/Snorlax', 'Inspired.png'))
        self.p_Nimg=load_image(os.path.join('asset/player/Quagsire', 'Normal.png'))
        self.p_Aimg = load_image(os.path.join('asset/player/Quagsire', 'Angry.png'))
        self.pp_Iimg = load_image(os.path.join('asset/player/Clodsire', 'Normal.png'))
    def update_state(self, new_state):
        self.state = new_state
    def check_progress(self,target_type):
        if self.target_type==target_type:
            self.current+=1
            #현재 진행도 표시
            print(self.pt+str(self.current)+"/"+str(self.target))
            if self.current>=self.target:
                self.state="complete"
                self.player.potion.type = 1
                return 1
        return 0
    def draw(self):
        if self.player.type == 1:
            self.p_Nimg.draw(110, 410, 200, 200)
        else:
            self.pp_Iimg.draw(110, 410, 200, 200)
        self.s_Cimg.draw(1290, 410, 200, 200)
        pass
    def change_step(self,new_step):
        self.step=new_step

class Q2:
    def __init__(self,player):
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
        self.player=player
        #누오 잠만보 이미지
        self.s_Nimg = load_image(os.path.join('asset/map/town/Snorlax', 'Normal.png'))
        self.s_Cimg = load_image(os.path.join('asset/map/town/Snorlax', 'Crying.png'))
        self.s_Iimg = load_image(os.path.join('asset/map/town/Snorlax', 'Inspired.png'))
        self.p_Nimg = load_image(os.path.join('asset/player/Quagsire', 'Normal.png'))
        self.p_Aimg = load_image(os.path.join('asset/player/Quagsire', 'Angry.png'))
        self.pp_Iimg = load_image(os.path.join('asset/player/Clodsire', 'Normal.png'))

    def update_state(self, new_state):
        self.state = new_state
    def check_progress(self,target_type):
        if self.target_type==target_type:
            self.current+=1
            # 현재 진행도 표시
            print(self.pt + str(self.current) + "/" + str(self.target))
            if self.current>=self.target:
                self.state="complete"
                self.player.potion.type = 2
                return 2
        return 0
    def draw(self):
        if self.player.type == 1:
            self.p_Nimg.draw(110, 410, 200, 200)
        else:
            self.pp_Iimg.draw(110, 410, 200, 200)
        self.s_Cimg.draw(1290, 410, 200, 200)
    def change_step(self,new_step):
        self.step=new_step
class Q3:
    def __init__(self,player):
        self.state = "intro"
        self.dialogues = {
            "intro": [],
            "progress": [],
            "complete": [],
        }
        self.dialogues["intro"] = load_dialogue('asset/map/town/Snorlax/quest/q3.txt')
        self.dialogues["progress"] = load_dialogue('asset/map/town/Snorlax/quest/process.txt')
        self.dialogues["complete"] = load_dialogue('asset/map/town/Snorlax/quest/q3_complete.txt')
        # intro → progress → complete
        self.target=1
        self.target_type = 98   #웅이 될건데 임시로 98해둠 나중에 바꿔야함
        self.current=0
        self.pt="연구원 처치 진행도: "
        self.step=0
        self.player=player
        # 누오 잠만보 이미지
        self.s_Nimg = load_image(os.path.join('asset/map/town/Snorlax', 'Normal.png'))
        self.s_Cimg = load_image(os.path.join('asset/map/town/Snorlax', 'Crying.png'))
        self.s_Iimg = load_image(os.path.join('asset/map/town/Snorlax', 'Inspired.png'))
        self.p_Nimg = load_image(os.path.join('asset/player/Quagsire', 'Normal.png'))
        self.p_Aimg = load_image(os.path.join('asset/player/Quagsire', 'Angry.png'))
        self.pp_Iimg = load_image(os.path.join('asset/player/Clodsire', 'Normal.png'))
    def update_state(self, new_state):
        self.state = new_state
    def check_progress(self,target_type):
        if self.target_type==target_type:
            self.current+=1
            #현재 진행도 표시
            print(self.pt+str(self.current)+"/"+str(self.target))
            if self.current>=self.target:
                self.state="complete"
                self.player.potion.type = 3
                return 2
        return 0
    def draw(self):
        if self.player.type == 1:
            self.p_Nimg.draw(110, 410, 200, 200)
        else:
            self.pp_Iimg.draw(110, 410, 200, 200)
        self.s_Cimg.draw(1290, 410, 200, 200)
        pass
    def change_step(self,new_step):
        self.step=new_step
class Q4:
    def __init__(self,player):
        self.state = "intro"
        self.dialogues = {
            "intro": [],
            "progress": [],
            "complete": [],
        }
        self.dialogues["intro"] = load_dialogue('asset/map/town/Snorlax/quest/q4.txt')
        self.dialogues["progress"] = load_dialogue('asset/map/town/Snorlax/quest/process.txt')
        self.dialogues["complete"] = load_dialogue('asset/map/town/Snorlax/quest/q4_complete.txt')
        # intro → progress → complete
        self.target=1
        self.target_type = 99   #웅이 될건데 임시로 98해둠 나중에 바꿔야함
        self.current=0
        self.pt="연구원 처치 진행도: "
        self.step=0
        self.player=player
        # 누오 잠만보 이미지
        self.s_Nimg = load_image(os.path.join('asset/map/town/Snorlax', 'Normal.png'))
        self.s_Cimg = load_image(os.path.join('asset/map/town/Snorlax', 'Crying.png'))
        self.s_Iimg = load_image(os.path.join('asset/map/town/Snorlax', 'Inspired.png'))
        self.p_Nimg = load_image(os.path.join('asset/player/Quagsire', 'Normal.png'))
        self.p_Aimg = load_image(os.path.join('asset/player/Quagsire', 'Angry.png'))
        self.pp_Iimg = load_image(os.path.join('asset/player/Clodsire', 'Normal.png'))
    def update_state(self, new_state):
        self.state = new_state
    def check_progress(self,target_type):
        if self.target_type == target_type:
            self.current += 1
            # 현재 진행도 표시
            print(self.pt + str(self.current) + "/" + str(self.target))
            if self.current >= self.target:
                self.state = "complete"
                return 2
        return 0
    def draw(self):
        if self.player.type == 1:
            self.p_Nimg.draw(110, 410, 200, 200)
        else:
            self.pp_Iimg.draw(110, 410, 200, 200)
        self.s_Cimg.draw(1290, 410, 200, 200)
        pass
    def change_step(self,new_step):
        self.step=new_step


class Q5:
    def __init__(self,player):
        self.state = "intro"
        self.dialogues = {
            "intro": [],
            "progress": [],
            "complete": [],
        }
        self.dialogues["intro"] = load_dialogue('asset/map/town/Snorlax/quest/q5.txt')
        self.dialogues["progress"] = load_dialogue('asset/map/town/Snorlax/quest/process.txt')
        self.dialogues["complete"] = load_dialogue('asset/map/town/Snorlax/quest/q5_complete.txt')
        # intro → progress → complete
        self.target = 1
        self.target_type = 99  #지우 될건데 임시로 98해둠 나중에 바꿔야함
        self.current = 0
        self.pt = "연구원 처치 진행도: "
        self.step = 0
        self.player=player
        # 누오 잠만보 이미지
        self.s_Nimg = load_image(os.path.join('asset/map/town/Snorlax', 'Normal.png'))
        self.s_Cimg = load_image(os.path.join('asset/map/town/Snorlax', 'Crying.png'))
        self.s_Iimg = load_image(os.path.join('asset/map/town/Snorlax', 'Inspired.png'))
        self.p_Nimg = load_image(os.path.join('asset/player/Quagsire', 'Normal.png'))
        self.p_Aimg = load_image(os.path.join('asset/player/Quagsire', 'Angry.png'))
        self.pp_Iimg = load_image(os.path.join('asset/player/Clodsire', 'Normal.png'))

    def update_state(self, new_state):
        self.state = new_state

    def check_progress(self, target_type):
        pass

    def draw(self):
        if self.player.type == 1:
            self.p_Nimg.draw(110, 410, 200, 200)
        else:
            self.pp_Iimg.draw(110, 410, 200, 200)
        self.s_Cimg.draw(1290, 410, 200, 200)
        pass

    def change_step(self, new_step):
        self.step = new_step
