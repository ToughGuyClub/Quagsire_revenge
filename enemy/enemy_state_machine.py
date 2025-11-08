class EnemyStateMachine:
    def __init__(self, start_state, rules):
        """
        start_state: 시작 상태 객체 (예: EnemyIdle(self))
        rules: 상태 전이 규칙 딕셔너리
                {
                    self.IDLE: { self.detect_player: self.RUN },
                    self.RUN: { self.lost_player: self.IDLE, self.in_attack_range: self.ATTACK },
                    self.ATTACK: { self.lost_player: self.IDLE }
                }
        """
        self.cur_state = start_state
        self.rules = rules
        self.cur_state.enter(player=None)  # 초기 상태 진입 시 더미 player 전달

    def update(self, player):
        """현재 상태를 수행하고, 전이 조건을 체크함."""
        # 1️⃣ 현재 상태 동작 실행
        result = self.cur_state.do(player)

        # 2️⃣ 상태 전이 조건 검사
        for check_func, next_state in self.rules[self.cur_state].items():
            try:
                if check_func(player):  # 조건 함수가 True면 전이 발생
                    self.cur_state.exit(player)
                    next_state.enter(player)
                    print(f"{self.cur_state.__class__.__name__} → {next_state.__class__.__name__}")
                    self.cur_state = next_state
                    break
            except Exception as e:
                print(f"[EnemyStateMachine Error] {e}")
        return result
    def draw(self):
        """현재 상태의 draw 호출"""
        self.cur_state.draw()
