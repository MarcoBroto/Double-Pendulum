from tkinter import Tk, Canvas, mainloop
from math import sin, cos, pi

windowWidth = 700
windowHeight = 500
origin = (windowWidth//2, windowHeight//2)  # Used for translation

master = Tk()
master.title('Double Pendulum')
cv = Canvas(master, width=windowWidth, height=windowHeight)
cv.pack()


g = 1  # Gravitational constant
m1, m2 = 40.0, 40.0  # Masses of pendulum orbs
L1, L2 = 100.0, 100.0  # Lengths of pendulum arms
t1, t2 = pi/2, pi/2  # Theta1 and Theta2
t1_vel, t2_vel = 0.0, 0.0 # Angular velocity
mu1, mu2 = 1, 1  # Coefficients of friction for theta1 and theta2
x1, y1 = 0,0 # Coordinate for first orb
x2, y2 = 0,0 # Coordinate for second orb

orb1Radius, orb2Radius = 11, 11
orb1, orb2, line1, line2 = None, None, None, None  # Saved canvas objects


def setup():
    cv.config(bg='black') # Set canvas background color

    # Set intitial orb points
    global x1, y1, x2, y2
    x1, y1 = L1*sin(t1), L1*cos(t1)
    x2, y2 = x1 + L2*sin(t2), y1 + L2*cos(t2)

    # Draw Pendulum
    global orb1, orb2, line1, line2
    l1ex, l1ey = origin[0] + x1, origin[1] + y1 # Used to speed up line coord update
    line1 = cv.create_line(origin[0], origin[1], l1ex, l1ey, fill="white")  # Line from Origin to First Orb
    line2 = cv.create_line(l1ex, l1ey, origin[0]+x2, origin[1]+y2, fill="white")  # Line from First Orb to Second Orb
    orb1 = cv.create_oval(l1ex-orb1Radius, l1ey-orb1Radius, l1ex+orb1Radius, l1ey+orb1Radius, fill="blue")  # First Orb
    orb2 = cv.create_oval(origin[0]+x2-orb2Radius, origin[1]+y2-orb2Radius, origin[0] + x2+orb2Radius, origin[1]+y2+orb2Radius, fill="red")  # Second Orb


def calcAngularAccel_RungeKutta():
    numer1: float = -g * (2*m1 + m2) * sin(t1)
    numer2: float = -m2 * g * sin(t1 - 2*t2)
    numer3: float = -2*sin(t1 - t2) * m2
    numer4: float = t2_vel**2 * L2 + t1_vel**2 * L1 * cos(t1 - t2)
    denom: float = L1 * (2*m1 + m2 - m2*cos(2*t1 - 2*t2))
    t1_acc: float = (numer1 + numer2 + numer3*numer4) / denom

    numer1: float = 2*sin(t1 - t2)
    numer2: float = t1_vel**2 * L1 * (m1 + m2)
    numer3: float = g * (m1 + m2) * cos(t1)
    numer4: float = t2_vel**2 * L2 * m2 * cos(t1 - t2)
    denom: float = L2 * (2*m1 + m2 - m2*cos(2*t1 - 2*t2))
    t2_acc: float = numer1 * (numer2 + numer3 + numer4) / denom

    return t1_acc, t2_acc


def draw():
    global t1, t2, t1_vel, t2_vel, x1, y1, x2, y2

    x1p, y1p, x2p, y2p = x1, y1, x2, y2 # Previous orb coordinates
    x1, y1 = L1*sin(t1), L1*cos(t1)
    x2, y2 = x1 + L2*sin(t2), y1 + L2*cos(t2)

    l1ex, l1ey = origin[0] + x1, origin[1] + y1 # Used to speed up line coord update
    cv.coords(line1, [origin[0], origin[1], l1ex, l1ey])
    cv.coords(line2, [l1ex, l1ey, origin[0]+x2, origin[1]+y2])
    cv.move(orb1, x1-x1p, y1-y1p)
    cv.move(orb2, x2-x2p, y2-y2p)
    cv.create_line(origin[0]+x2p, origin[1]+y2p, origin[0]+x2, origin[1]+y2, fill='orange') # Path tracing line
    # cv.create_oval(origin[0]+x2p, origin[1]+y2p, origin[0]+x2p+1, origin[1]+y2p+1, fill='white') # Path tracing dots

    try:
        t1_acc, t2_acc = calcAngularAccel_RungeKutta()
        t1_vel = (t1_vel + t1_acc) * mu1
        t2_vel = (t2_vel + t2_acc) * mu2
        t1 += t1_vel
        t2 += t2_vel
    except OverflowError:
        print(f'Overflow Error!\nState values: {t1=}, {t2=}, {t1_vel=}, {t2_vel=}')
        return

    cv.update()
    cv.after(0, draw)


def main():
    setup()
    draw()
    mainloop()

if __name__ == '__main__': main()
