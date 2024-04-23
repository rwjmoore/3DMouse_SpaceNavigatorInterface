import spacenav
from collections import namedtuple
import time
import threading 
import numpy as np
import matplotlib.pyplot as plt

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
relativePose_np = np.zeros(6)
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
    success = spacenav.open()
    print("\n\nSpaceNavigator3DPose")

    if success:
        while True:
            state = spacenav.read()
            with lock:
                relativePose = state
                i += 1
            time.sleep(0.01)

# ------------->                End                   <-------------------

# -------------> Signal Processing Functions <--------------------
def mapMouseToPose(state):
    pose = np.zeros(6)

    d = 0.05 #deadband threshold
    beta = 0.5 #cubic sensitivity parameter 
    #map deadbands 
    pose[0] = deadBand(state.x,d,beta)
    pose[1] = deadBand(state.y,d,beta)
    pose[2] = deadBand(state.z,d,beta)
    pose[3] = deadBand(state.pitch,d,beta)
    pose[4] = deadBand(state.yaw,d,beta)
    pose[5] = deadBand(state.roll,d,beta)

    #scale and map to holoLens coordinate system
    k_poseTrans = 0.005 #gain for pose translation 
    pose[0] = k_poseTrans*state.x
    pose[1] = k_poseTrans*state.y
    pose[2] = k_poseTrans*state.z
    #map linear region [-1,1] to [-10,10] degrees 
    k_poseRot = 10
    pose[3] =  k_poseRot*state.roll
    pose[4] =  k_poseRot*state.pitch
    pose[5] =  k_poseRot*state.yaw

    return pose

#d = threshold for deadband region , beta is cubic sensitivity transformation parameter 
def deadBand(x, d, beta):
    if abs(x) < d:
        return 0 
    return ( cubicSensitivtyFunction(x,beta) -  np.sign(x)*cubicSensitivtyFunction(d,beta) ) / ( 1 - cubicSensitivtyFunction(d,beta) )
    

def cubicSensitivtyFunction(x,beta):
    return beta*x**3 + (1 - beta)*x

#TEST FUNCTION
def generateRange(start, end, step):
    num = np.linspace(start, end,(end-start)
                      *int(1/step)+1).tolist()
    return [round(i, 2) for i in num]
# ------------> Signal Processing Functions End <-------------------


# ----->                    Main Loop           <-----------
if __name__ == '__main__':

    #TEST FOR MAPPING ACCURACY
    #output mapping visualization 
    x = generateRange(-1,1,0.0001)
    y = [] 
    for i in range(1,len(x)):
        y.append(deadBand(x[i],0.1,0.5))
    plt.plot(y)
    plt.show()

    t1 = threading.Thread(target=callback)
    t1.daemon = True
    t1.start()
    try: 
        while True:
            with lock:
                print3DmouseState(relativePose)
                
            time.sleep(0.001)
    except KeyboardInterrupt:
        pass
    

