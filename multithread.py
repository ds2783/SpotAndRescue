import threading
import subprocess

def runScript(fname):
	subprocess.run(['python', fname])
	
if __name__ == "__main__":
	s1 = threading.Thread(target=runScript, args=("lidar.py",))
	s2 = threading.Thread(target=runScript, args=("test.py",))
	s3 = threading.Thread(target=runScript, args=("UI.py",))
	s4 = threading.Thread(target=runScript, args = ("webcam.py",))
	
	s1.start()
	s2.start()
	s3.start()
	s4.start()
	
	s1.join()
	s2.join()
	s3.join()
	s4.join()
