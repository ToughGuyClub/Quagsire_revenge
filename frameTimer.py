import time

# 프레임 타이밍용 변수
current_time = time.time()
frame_time = 0.0

def get_frame_time():
    global current_time, frame_time
    now = time.time()
    frame_time = now - current_time
    current_time = now
    return frame_time