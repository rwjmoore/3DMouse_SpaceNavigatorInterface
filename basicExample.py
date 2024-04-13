import spacenavigator
import time

success = spacenavigator.open()
if success:
    spacenavigator.set_led(1)
    try:
        while 1:
            state = spacenavigator.read()
            #t,x,y,z,pitch,yaw,roll,button
            print(f"t:{state.t:.2f}  x: {state.x:.2f} y: {state.y:.2f} z: {state.z:.2f} pitch: {state.pitch:.2f} yaw: {state.yaw:.2f} roll: {state.roll:.2f} button: " + str(state.buttons) )   
            # print(state)
            time.sleep(0.01)
    except:
        spacenavigator.set_led(0)


def print3DmouseState(state):
    print(f"t:{state.t:.2f}  x: {state.x:.2f} y: {state.y:.2f} z: {state.z:.2f} pitch: {state.pitch:.2f} yaw: {state.yaw:.2f} roll: {state.roll:.2f} button: " + str(state.buttons) )   

