class QuestManager:
    def __init__(self):
        self.current_quest = "q1"
        self.quest_state = "intro"
        # intro, progress, complete 등

    def get_dialogue_file(self, npc_id):
        # 예: npc_id = "snorlax"

        quest = self.current_quest
        state = self.quest_state

        # q1_intro, q1_progress, q1_complete 이런 식으로 파일명 만든다
        filename = f"{npc_id}/{quest}_{state}.txt"
        return filename

    def on_dialogue_end(self):
        """대화 종료 후 퀘스트를 어떻게 진행시킬지 결정"""
        if self.current_quest == "q1" and self.quest_state == "intro":
            self.quest_state = "progress"

        elif self.current_quest == "q1" and self.quest_state == "complete":
            self.current_quest = "q2"
            self.quest_state = "intro"

        # 계속 추가 가능
