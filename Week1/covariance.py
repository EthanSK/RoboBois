from math import sqrt

def main():

    xcoords = [0,0,0,2,0,0,1,0,0,1]
    ycoords = [0,0,0,2,0,0,3,0,0,1]

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