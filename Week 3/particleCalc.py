import movement
import sensor
import robot
import brickpi3
import time
import math

import weightedParticles as ptcls

def particles():

    motor_port_left = brickpi3.BrickPi3.PORT_D
    motor_port_right = brickpi3.BrickPi3.PORT_A
    touch_port_left = brickpi3.BrickPi3.PORT_4
    touch_port_right = brickpi3.BrickPi3.PORT_1
    sonar_port = brickpi3.BrickPi3.PORT_2

    wheel_radius = 3.5 / 100 # 3.5cm
    body_radius = 7.1 / 100 # cm

    movement_module = movement.MovementModule(motor_port_left, motor_port_right, wheel_radius, body_radius)
    sensor_module = sensor.SensorModule(touch_port_left, touch_port_right, sonar_port)
    roboboi = robot.Robot(movement_module, sensor_module)

    scatterList = [(0,0,0)] * 100    
    xdist = 10
    ydist = 0

    try:
        for i in range(4):

            if(i == 0): 
                xdist = 10
                ydist = 0
            elif(i == 1):
                xdist = 0
                ydist = 10
            elif(i == 2):
                xdist = 10
                ydist = 0
            elif(i == 3):
                xdist = 0
                ydist = 10

            for x in range(4):
                roboboi.movement_module.move_linear(0.1, -0.05)
                
                for j in range(len(scatterList)):   
                    scatterList[j] = ptcls.straightLineWeightedParticles(scatterList[j][0],
                        scatterList[j][1], scatterList[j][2],
                        xdist, ydist, 0.06, 0.06, 0.00)
                
                newList = [(0,0,0)] * 100
                for q in range(len(newList)):
                    newList[q] = (((scatterList[q][0] * 10) + 50), ((scatterList[q][1] * -10) + 450), (scatterList[q][2]))
                time.sleep(1)
                print("drawLine:" + str((50,50,450,50)))
                print("drawLine:" + str((450,50,450,450)))
                print("drawLine:" + str((450,450,50,450)))
                print("drawLine:" + str((50,450,50,50)))
                print("drawParticles:" + str(newList))

            roboboi.movement_module.turn(90)
            for j in range(len(scatterList)):   
                scatterList[j] = ptcls.rotationWeightedParticles(scatterList[j][0],
                    scatterList[j][1], scatterList[j][2],
                    (math.pi/2), 0.00)


            newList = [(0,0,0)] * 100
            for q in range(len(newList)):
                newList[q] = (((scatterList[q][0] * 10) + 50), ((scatterList[q][1] * -10) + 450), (scatterList[q][2]))
            time.sleep(1)
            print("drawLine:" + str((50,50,450,50)))
            print("drawLine:" + str((450,50,450,450)))
            print("drawLine:" + str((450,450,50,450)))
            print("drawLine:" + str((50,450,50,50)))            
            
            print("drawParticles:" + str(newList))


    except KeyboardInterrupt:
        roboboi.reset()

if __name__ == "__main__":
    particles()




