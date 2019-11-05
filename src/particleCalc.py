import movement
import sensor
import robot
import brickpi3
import time

import weightedParticles as ptcls

def particles():

    motor_port_left = brickpi3.BrickPi3.PORT_D
    motor_port_right = brickpi3.BrickPi3.PORT_A
    touch_port_left = brickpi3.BrickPi3.PORT_4
    touch_port_right = brickpi3.BrickPi3.PORT_1
    sonar_port = brickpi3.BrickPi3.PORT_2

    wheel_radius = 3.5 / 100 # 3.5cm
    body_radius = 6.5 / 100 # cm

    movement_module = movement.MovementModule(motor_port_left, motor_port_right, wheel_radius, body_radius)
    sensor_module = sensor.SensorModule(touch_port_left, touch_port_right, sonar_port)
    roboboi = robot.Robot(movement_module, sensor_module)

    scatterList = [(0,0,0)] * 100

    try:
        for i in range(4):
            
            if(i == (1 or 3)): 
                xdist = 10
                ydist = 0
            elif(i == (2 or 4)):
                xdist = 0
                ydist = 10

            for x in range(4):
                roboboi.movement_module.move_linear(0.1, 0.05)
                
                for j in range(len(scatterList)):   
                    scatterList[j] = ptcls.straightLineWeightedParticles(scatterList[j][0],
                        scatterList[j][1], scatterList[j][2],
                        xdist, ydist, 0.06, 0.275, 0.08)

                print("Particle output", scatterList)

            roboboi.movement_module.turn(90)
            for j in range(len(scatterList)):   
                scatterList[j] = ptcls.rotationWeightedParticles(scatterList[j][0],
                    scatterList[j][1], scatterList[j][2],
                    90, 0.08)

            print("Particle output (rotation)", scatterList)


    except KeyboardInterrupt:
        roboboi.reset()

if __name__ == "__main__":
    particles()