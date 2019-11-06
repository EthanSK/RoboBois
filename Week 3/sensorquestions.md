# 2.3.1 Sonar Calibration Questions to Answer

* When placed facing and perpendicular to a smooth surface such as a wall, what are the minimum and maximum depths that the sensor can reliably measure?

Min:
-Slight issues below 25cm - 2cm standard deviation
-Gets worse at 15cm
-Below 10cm completely breaks

Max:
-254.99999999999997cm - is this because it's 8 bit?

* Move the sonar so that it faces the wall at a non-orthogonal incidence angle. What is the maximum angular deviation from perpendicular to the wall at which it will still give sensible readings?

90: 53.0cm
45: 43.0cm
70: 50cm
75: 51cm
80: 52cm

-> 70 is the threshold beyond which we will disregard values

* Do your sonar depth measurements have any systematic (non-zero mean) errors? To test this, set up the sensor at a range of hand-measured depths (20cm, 40cm, 60cm, 80cm, 100cm) from a wall and record depth readings. Are they consistently above or below what they should be?

20: 22
40: 40
60: 60
80: 80  
100: 100

* What is the the accuracy of the sonar sensor and does it depend on depth? At each of two chosen hand-measured depths (40cm and 100cm make 10 separate depth measurements (each time picking up and replacing the sensor) and record the values. Do you observe the same level of scatter in each case?

40:
```bash
1: 40 
2: 40
3: 40
4: 40
5: 40
6: 40
7: 40
8: 40
9: 40
10: 40
```

100:
```bash
1: 100
2: 100
3: 100
4: 100
5: 100
6: 100
7: 100
8: 100
9: 100
10: 100
```


* In a range of general conditions for robot navigation, what fraction of the time do you think your sonar gives garbage readings very far from ground truth?

If we assume reasonable limits - such as a maze where no distance can be further than 255cm (i.e. upper bound is constrained), but no limit on the short distance - and we assume that the robot is likely to be always perpendicular to a wall & equally distributed around the maze, then we can assume that 25/255 measurements are bogus or ~10%.

