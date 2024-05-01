import spacenav
import time

success = spacenav.open(device = "SpaceMouse Navigator For Notebooks")
spacenav.set_led(0)
if success:
    try:
        while 1:
            state = spacenav.read()
            #t,x,y,z,pitch,yaw,roll,button
            print(f"t:{state.t:.2f}  x: {state.x:.2f} y: {state.y:.2f} z: {state.z:.2f} pitch: {state.pitch:.2f} yaw: {state.yaw:.2f} roll: {state.roll:.2f} button: " + str(state.buttons) )   
            # print(state)
            time.sleep(0.01)
    except:
        
        print("error")


def print3DmouseState(state):
    print(f"t:{state.t:.2f}  x: {state.x:.2f} y: {state.y:.2f} z: {state.z:.2f} pitch: {state.pitch:.2f} yaw: {state.yaw:.2f} roll: {state.roll:.2f} button: " + str(state.buttons) )   

