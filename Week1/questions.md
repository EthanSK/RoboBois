## Q2
* What happens in each case if you use your hand to try to gently slow down the running motor, and what can you observe in the power and velocity of the motor, and why?  

Power: Following motor is power consistent in the face of resistance. The following's power corresponds directly, we assume by a mapping, to the angle that leading is rotated to (if we assume that it starts at 0 degrees).

Position: The following motor will keep trying to follow the leading motor, even after being held still while the leading motor moves. As for velocity, the following motor keeps consistent velocity regardless of position distance between following and leading. Power is also consistent, regardless of resistance, so more resistance means less velocity.  

DPS: Behaves similarly to Power in how it gets its power and thus velocity; however, there is a difference in the face of resistance. The motor puts in more power to overcome resistance, as it's trying to match velocity - this leads to excessively high current that causes the BrickPi's anti-overcurrent failsafe to kick in.

## Q4
* What is the approximate scatter range of the different outcomes? 
The standard deviation in the x-direction is 0.255cm, and in the y-direction is 0.5cm. 

* Is there a systematic error (meaning that the final locations are consistently different from the ideal result with an error in the same direction)? 
Yes, we believe that the non-zero covariance implies that there is a minor systematic error in our robot. Unfortunately we were not able to completely eliminate this, although we considered implementing a software bias.

* Is there much scatter, such that the points are quite spread out from each other?
No, despite slight innacuracy the robot is very precise. We were pleased with this, and we believe this is due to our delicate calibration.

## Q5
* Why do we have covariance as well as just the normal variance?
Because this shows the effect of both co-ordinates on each other - we're using two dimensions, and often scatter ends up being something like an oval instead of a pure circle. Thus, the covariance provides us with an insight into underlying biases and imprecision in the robot's movement.

## Further Thought
* Which causes a larger effect on your robot, imprecision in drive distance or rotation angle?
Rotation angle. We believe this is due to sag in the robot's structure, which effectively shortens the distance between the wheels' point of contact with the ground and thus makes the calculations slightly inaccurate. 

* Can you think of any robot designs which would be able to move more precisely?
Yes, more wheels might help as this would add to stability and allow more proprioceptive sensing. More precisely made kit than lego would also be advantageous.

* How should we go about equipping a robot to recover from the motion drift we have observed in this experiment?
There are multiple ways to do this. This includes: 
- Using a Gyro sensor to double-check rotations
- Using Visual closed-loop control (servoing) to check location
- Same with laser range-finding

## Results

```bash
ycoords = [-0.25, -0.10, 0.35, 0.60, 0.60, 0.90, 0.85, 1.10, 1.30, 1.40] 
xcoords = [-0.05, -0.35, -0.40, -0.20, -0.50, -0.25, -0.65, -0.60, -1.00, -0.35]

mean final location:  -0.43499999999999994 , 0.675
sqrts:  0.255 , 0.5245235933683059
0.065025  |  -0.080375
-0.080375  |  0.27512499999999995
```
