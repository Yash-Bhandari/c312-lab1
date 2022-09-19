import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from equations import *
import math

# ===========================================

# == Wheel Speed plt ==
fig2, ax2 = plt.subplots()
barcollection = plt.bar(['v_l', 'v_r', 'R'],[0, 0, 0])

# == Graph of curve plt ==
fig1, ax1 = plt.subplots()
ln, = plt.plot([], [], lw=2)
ln2, = plt.plot([], [], lw=2)
ln3, = plt.plot([], [], 'o')

# ===========================================
# == Constants ==
d = 0.0575 # distance between wheels over 2 -- meters
wheel_circumference = 0.221 # -- meters
frac = 1/2
DriveTime = 2*np.pi * 1/frac # -- seconds
NoneTime = np.pi/2
totTime = NoneTime*2+DriveTime
Steps = int(math.ceil(30 * totTime/np.pi)) # 30 steps per pi sec
timeStep = totTime/Steps # time per step
v_l, v_r = [], []

# ===========================================
# == inital curve ==
t = np.linspace(-NoneTime+np.pi, DriveTime+NoneTime+np.pi, Steps)
x, y = lemniscate(t, 1/2, frac) # time, scale, frac
# x,y = circle(t, 1/16, 1.5)

# ===========================================
# == derivatives of curve ==
dir_x_1, dir_x_2, dir_y_1, dir_y_2 = derivatives(x,y,t)

# ===========================================
# == Radius of curvature == (meters) ==
R = ((dir_x_1**2 + dir_y_1**2)**(3/2)/
        (dir_x_1*dir_y_2 - dir_x_2*dir_y_1))

# ===========================================
# == arc length & speed of curve == (meters) ==
V = np.sqrt(dir_x_1**2 + dir_y_1**2)  # m/s
arcLenght = np.trapz(V, x=t)
print(arcLenght)

# s = np.array([0])
# for i in range(1,len(t0)):
#     arcLenght = np.trapz(V_old[0:i], x=t0[0:i])
#     s = np.append(s,arcLenght)
# print(s)
# frac = 1
# x, y = lemniscate(s, 1, totTime/s[-1])"""

# """# ===========================================
# # == derivatives ==
# dir_x_1, dir_x_2, dir_y_1, dir_y_2 = derivatives(x,y,s)

# # ===========================================
# # == New Velocities ==
# V = np.sqrt(dir_x_1**2 + dir_y_1**2) # m/s
# print(V)


def init():
    ax1.set_xlim(-1, 1)
    ax1.set_ylim(-1, 1)
    ln.set_data(x, y)
    return ln,ln2,ln3


def update(i):
    global R
    circle_center_x = ( x[i] +
                        R[i]/((dir_x_1[i]**2 + dir_y_1[i]**2)**(1/2)) *
                        -1 * dir_y_1[i] )

    circle_center_y = ( y[i] +
                        R[i]/((dir_x_1[i]**2 + dir_y_1[i]**2)**(1/2)) *
                        dir_x_1[i] )

    circle_x = circle_center_x + abs(R[i])*np.cos(t)
    circle_y = circle_center_y + abs(R[i])*np.sin(t)

    ln2.set_data(circle_x, circle_y) # draw circle
    ln3.set_data(x[i], y[i]) # draw curve

    return ln, ln2, ln3


def init2():
    ax2.set_ylim(-60, 60)


def update2(i):
    global R

    v_left = V[i] - (V[i]*d)/R[i]
    v_right = 2*V[i] - v_left

    v_left = FakeSpeedToRealSpeed(v_left)
    v_right = FakeSpeedToRealSpeed(v_right)


    print('V {:.3f}, V_l {:.3f}, V_r {:.3f}, R {:.3f}, V{:.3f}'.format(
           V[i], v_left, v_right, R[i], (v_left+v_right)/2))

    barcollection[0].set_height(v_left)
    barcollection[1].set_height(v_right)
    barcollection[2].set_height(R[i])

    v_l.append(v_left)
    v_r.append(v_right)

    return barcollection

def RealWheelSpeed(v): # probably wrong
    return (v*10*np.pi*wheel_circumference)/180

def FakeSpeedToRealSpeed(v):
    return ((v/wheel_circumference)*360)/10


# ===========================================
# == Plot graphs ==
anim2 = FuncAnimation(fig2, update2, frames=Steps,
                      init_func=init2, repeat=False)

ani1 = FuncAnimation(fig1, update, frames=Steps,
                    init_func=init, blit=True, repeat=False)

plt.show()

# ===========================================
# == Save graph data ==
with open('curve.txt', 'w') as f:
    for i in range(len(t)):
        f.write(str(v_l[i]) + ' ' + str(v_r[i]) + ' ' + str(timeStep))
        f.write('\n')
f.close()


# def wheelSpeed(v_l, v_r):
#     if abs(v_l) > maxSpeed:
#         s = np.sign(v_r)
#         factor = v_l/maxSpeed

#         v_l /= factor
#         v_r /= s*factor

#     if abs(v_r) > maxSpeed:
#         s = np.sign(v_l)
#         factor = v_r/maxSpeed

#         v_r /= s*factor
#         v_r /= factor

#     return v_l, v_r
