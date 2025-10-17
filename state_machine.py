from event_to_string import event_to_string

class StateMachine:
    def __init__(self, start_state,rules):
        self.cur_state = start_state
        self.rules = rules
        #self.cur_state.enter(None) #시작할 때 더미로 쓰는거


    def update(self,current_map,event=None):

        self.cur_state.do(event, current_map)
    def draw(self):
        self.cur_state.draw()

    def handle_state_event(self, state_event,current_map):
        # state_event가 어떤 이벤트인지 체크할 수 있어야함
        for check_event in self.rules[self.cur_state].keys(): #<-rules[현재상태]하면 Dict가 나옴.keys하면 키가 나옴
            if check_event(state_event):    #<-체크이벤트를 호출하면 spacedown이 넘어옴
                self.next_state = self.rules[self.cur_state][check_event] #<-다음상태를 가져옴
                self.cur_state.exit(state_event) #<-현재상태에서 exit호출
                self.next_state.enter(state_event) #<-다음상태에서 enter호출
                print(f"{event_to_string(state_event)}: {self.cur_state.__class__.__name__} -> {self.next_state.__class__.__name__}")
                self.cur_state = self.next_state #<-현재상태를 다음상태로 변경
                return
        #이벤트에 대한 처리가 안됨
        print(f'처리되지 않은 이벤트 {event_to_string(state_event)}')

