import spacenavigator
import time

success = spacenavigator.open()
if success:
    while 1:
        state = spacenavigator.read()
        print(state.x, state.y, state.z)
        time.sleep(0.01)