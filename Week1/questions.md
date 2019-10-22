## Q2
* What happens in each case if you use your hand to try to gently slow down the running motor, and what can you observe in the power and velocity of the motor, and why?  

Power: Following motor is power consistent, and velocity consistent, in the face of resistance. The following's power corresponds directly, we assume by a mapping, to the angle that leading is rotated to (if we assume that it starts at 0 degrees).

Position: The following motor will keep trying to follow the leading motor, even after being held still while the leading motor moves. As for velocity, the following motor keeps consistent velocity regardless of position distance between following and leading. Power is also consistent, regardless of resistance, so more resistance means less velocity.  

DPS: Behaves similarly to Power in how it gets its power and thus velocity; however, there is a difference in the face of resistance. The motor puts in more power to overcome resistance, as it's trying to match velocity - this leads to excessively high current that causes the BrickPi's anti-overcurrent failsafe to kick in.

## Q4
* What is the approximate scatter range of the different outcomes? 
* Is there a systematic error (meaning that the final locations are consistently different from the ideal result with an error in the same direction)? 
* Is there much scatter, such that the points are quite spread out from each other?

## Q5
* Why do we have covariance as well as just the normal variance?
Because this shows the effect of both co-ordinates on each other - we're using two dimensions, and often scatter ends up being something like an oval instead of a pure circle. Thus, the covariance provides us with an insight into underlying biases and imprecision in the robot's movement.

## Further Thought
* Which causes a larger effect on your robot, imprecision in drive distance or rotation angle?
* Can you think of any robot designs which would be able to move more precisely?
* How should we go about equipping a robot to recover from the motion drift we have observed in this experiment?
Gyro sensor? Line tracing with colour sensor?
