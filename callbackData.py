import spacenavigator
from collections import namedtuple
import time
import threading 

# -------------> Defining DataStructure for 6DOF Mouse Input <-------------------
dict_state = {
            "t": -1,
            "x": 0,
            "y": 0,
            "z": 0,
            "roll": 0,
            "pitch": 0,
            "yaw": 0,
            "buttons": [0,0],
        }

# tuple for 6DOF results
SpaceNavigator = namedtuple(
    "SpaceNavigator", ["t", "x", "y", "z", "roll", "pitch", "yaw", "buttons"]
)
relativePose =SpaceNavigator(**dict_state)
# ------------->                    End                     <-------------------

i = 0
lock = threading.Lock()

# ------------->                Callbacks                   <-------------------

def button_0(state, buttons, pressed_buttons):
    print("Button:", pressed_buttons)


def button_0_1(state, buttons, pressed_buttons):
    print("Buttons:", pressed_buttons)


def someButton(state, buttons):
    print("Some button")

def print3DmouseState(state):
    # tuple for 6DOF results

    print(f"t:{state.t:00.2f}  x: {state.x:.2f} y: {state.y:.2f} z: {state.z:.2f} pitch: {state.pitch:.2f} yaw: {state.yaw:.2f} roll: {state.roll:.2f} button: " + str(state.buttons), end='\r', flush=True )   
    

def callback():
    # button_arr = [spacenavigator.ButtonCallback(0, button_0),
    #               spacenavigator.ButtonCallback([1], lambda state, buttons, pressed_buttons: print("Button: 1")),
    #               spacenavigator.ButtonCallback([0, 1], button_0_1), ]
    global i
    global relativePose
    success = spacenavigator.open()
    print("\n\nSpaceNavigator3DPose")

    if success:
        while True:
            state = spacenavigator.read()
            with lock:
                relativePose = state
                i += 1
            time.sleep(0.01)

# ------------->                End                   <-------------------





# ----->                    Main Loop           <-----------
if __name__ == '__main__':
    t1 = threading.Thread(target=callback)
    t1.daemon = True
    t1.start()
    try: 
        while True:
            with lock:
                print3DmouseState(relativePose)
                # print(i)
            time.sleep(0.001)
    except KeyboardInterrupt:
        pass
    

