import pybullet as p
import pybullet_data
import time
import random
import math

p.connect(p.GUI)
p.setGravity(0, 0, -9.81)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

plane = p.loadURDF("plane.urdf")
p.changeVisualShape(plane, -1, rgbaColor=[0.8, 0.35, 0.2, 1])

rover_collision = p.createCollisionShape(
    p.GEOM_BOX,
    halfExtents=[0.4, 0.3, 0.1]
)

rover_visual = p.createVisualShape(
    p.GEOM_BOX,
    halfExtents=[0.4, 0.3, 0.1],
    rgbaColor=[0.7, 0.7, 0.7, 1]
)

rover = p.createMultiBody(
    baseMass=5,
    baseCollisionShapeIndex=rover_collision,
    baseVisualShapeIndex=rover_visual,
    basePosition=[0, 0, 0.2]
)

ball_collision = p.createCollisionShape(
    p.GEOM_SPHERE,
    radius=0.15
)

ball_visual = p.createVisualShape(
    p.GEOM_SPHERE,
    radius=0.15,
    rgbaColor=[0, 1, 0, 1]
)

ball = None

def spawn_ball():
    global ball

    if ball is not None:
        p.removeBody(ball)

    x = random.uniform(-5, 5)
    y = random.uniform(-5, 5)

    ball = p.createMultiBody(
        baseMass=0,
        baseCollisionShapeIndex=ball_collision,
        baseVisualShapeIndex=ball_visual,
        basePosition=[x, y, 0.15]
    )

spawn_ball()

while True:

    rover_pos, _ = p.getBasePositionAndOrientation(rover)
    ball_pos, _ = p.getBasePositionAndOrientation(ball)

    dx = ball_pos[0] - rover_pos[0]
    dy = ball_pos[1] - rover_pos[1]

    distance = math.sqrt(dx * dx + dy * dy)

    if distance < 0.7:
        spawn_ball()

    else:
        speed = 2.0

        vx = speed * dx / distance
        vy = speed * dy / distance

        p.resetBaseVelocity(
            rover,
            linearVelocity=[vx, vy, 0]
        )

    p.stepSimulation()
    time.sleep(1 / 240)