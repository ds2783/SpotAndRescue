from evdev import InputDevice, categorize, ecodes
import os
import time
from ServoController import ServoController
import Locomotion
import numpy as np
import asyncio
import time

# Change this path to match your keyboard device (check with `ls /dev/input/`)
dev = InputDevice('/dev/input/event0')
global locomotion
# Start Trotting

#arm=[12,13,14,15]
arm={12:90,13:150,14:100,15:60}


controller = ServoController()

ports = [0, 1, 2, 3,4,5,6,7,8,9,10,11,12,13,14,15]
#offsets = np.loadtxt("config.csv", delimiter=",", dtype=int)
offsets = np.zeros(16)

servos = controller.load_servos(ports, offsets)
locomotion = Locomotion.Locomotion(servos)
# Configure leg servos to use a wider range
for i in range(len(servos)):
	servos[i].set_min_angle(22.5)
	servos[i].set_min_pulse(.5 / ((1/50.0)/4096 * 1e3))
	servos[i].set_max_angle(157.5)
	servos[i].set_max_pulse(2.5 / ((1/50.0)/4096 * 1e3))
	
for port,angle in arm.items():
    servos[port].set_angle(angle)
	
locomotion.toggle_standing()

async def Moving_Forward():
    await asyncio.sleep(1)
    locomotion.toggle_standing()
    servos[14].set_angle(180)
    
    # Walk Forward
    locomotion.set_forward_factor(1.0)
    await asyncio.sleep(3)
    locomotion.Shutdown()
    

 

async def Moving_Backward():
    await asyncio.sleep(1)
    locomotion.toggle_standing()
    servos[14].set_angle(60)
    
    # Walk Forward
    locomotion.set_forward_factor(-1.0)
    await asyncio.sleep(3)
    locomotion.Shutdown()
    
loop = asyncio.get_event_loop()
print(f"Reading input from {dev}")

async def main1():
    locomotion_task = asyncio.create_task(locomotion.Run())
    test_task = asyncio.create_task(Moving_Forward())
    
    await locomotion_task
    await test_task

async def main2():
    locomotion_task = asyncio.create_task(locomotion.Run())
    test_task = asyncio.create_task(Moving_Backward())
    
    await locomotion_task
    await test_task

def move_up():
    print("\nMoving up!")
    asyncio.run(main1())
    time.sleep(2)
    
def move_down():
    print("\nMoving down!")
    asyncio.run(main2())
    time.sleep(2)
    
def move_left():
    print("\nMoving left!")
    

def move_right():
    print("\nMoving right!")


def exit_program():
    print("Exiting program...")
    os.system("pkill -f your_program_name")  # Replace with the command to exit the program you want

def main():
	
	for event in dev.read_loop():
		if event.type == ecodes.EV_KEY:
			key_event = categorize(event)
			
			if key_event.keystate == 1:  # Key down event
				if key_event.keycode == 'KEY_UP':
					move_up()
				elif key_event.keycode == 'KEY_DOWN':
					move_down()
				elif key_event.keycode == 'KEY_ESC':
					locomotion.toggle_standing()
					locomotion.Shutdown()
					exit_program()
					break  # Exit the loop to end the program
					
if __name__ == "__main__":
	main()
