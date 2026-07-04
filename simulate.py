import pybullet as p
import time

physicsClient = p.connect(p.GUI)

for iteration in range(1000):
	p.stepSimulation()
	time.sleep(1/60)
	print(iteration)
p.disconnect()