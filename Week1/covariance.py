from math import sqrt

def main():

    # units in cm
    ycoords = [-0.25, -0.10, 0.35, 0.60, 0.60, 0.90, 0.85, 1.10, 1.30, 1.40] 
    xcoords = [-0.05, -0.35, -0.40, -0.20, -0.50, -0.25, -0.65, -0.60, -1.00, -0.35]

    N = len(xcoords)
    if(N != len(ycoords)): exit(1)

    xmean = sum(xcoords)/N
    ymean = sum(ycoords)/N

    varx = 0
    vary = 0
    covxy = 0
    covyx = 0

    for i in range(0,N):
        varx += (xcoords[i]-xmean)**2
        vary += (ycoords[i]-ymean)**2
        covxy += (xcoords[i]-xmean)*(ycoords[i]-ymean)
        covyx += (ycoords[i]-ymean)*(xcoords[i]-xmean)
    
    varx /= N
    vary /= N
    covxy /= N
    covyx /= N

    print("mean final location: ", xmean, ",", ymean)
    print("sqrts: ", sqrt(varx), ",", sqrt(vary))
    print(varx, " | ", covxy)
    print(covyx, " | ", vary)

if __name__ == "__main__":
    main()