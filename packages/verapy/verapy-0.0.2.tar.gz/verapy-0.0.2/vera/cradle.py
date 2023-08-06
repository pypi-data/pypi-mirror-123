import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

G = 9.8
L = 3  # length of the pendulum
period = 2 * np.pi * np.sqrt(L / G)
t_stop = 2 * period  # how many seconds to simulate
initialAngle = 0.8  # radians


# create a time array from 0..t_stop sampled at dt second steps
dt = 0.03
t = np.arange(0, t_stop, dt)

fig = plt.figure(figsize=(5, 4), constrained_layout=True)
ax = fig.add_subplot(autoscale_on=False, xlim=(-4, 4), ylim=(-4, 0))
ax.set_aspect('equal')
ax.axis('off')

line1, = ax.plot([], [], 'k-', lw=2, zorder=-1)
line2, = ax.plot([], [], 'k-', lw=2, zorder=-1)

left_offset = -0.5
right_offset = 0.5

circle1 = plt.Circle((left_offset, -L), radius=0.55, color='gold')
circle2 = plt.Circle((right_offset, -L), radius=0.55, color='deepskyblue')

ve = ax.annotate("ve", xy=(left_offset, -L), fontsize=34, ha='center',
                 va='center', color='w')
ra = ax.annotate("ra", xy=(right_offset, -L), fontsize=34, ha='center',
                 va='center', color='w')

ax.add_patch(circle1)
ax.add_patch(circle2)


def animate(i):
    theta = initialAngle * np.cos((G / L)**(1 / 2) * t[i])

    x = min(left_offset, left_offset + L * np.sin(theta))
    if x == left_offset:
        y = - L
    else:
        y = -L * np.cos(theta)
    leftx = [left_offset, x]
    lefty = [0, y]
    circle1.set_center((x, y))
    ve.set_position((x, y))
    ve.set_rotation(min(0, np.rad2deg(theta)))


    x = max(right_offset, right_offset + L * np.sin(theta))
    if x == right_offset:
        y = - L
    else:
        y = -L * np.cos(theta)
    rightx = [right_offset, x]
    righty = [0, y]
    circle2.set_center((x, y))
    ra.set_position((x, y))
    ra.set_rotation(max(0, np.rad2deg(theta)))

    line1.set_data(leftx, lefty)
    line2.set_data(rightx, righty)

    return line1, line2, circle1, circle2, ve, ra


ani = animation.FuncAnimation(fig, animate, len(t), interval=dt * 1000,
                              blit=True)
print('saving...')
ani.save('vera.gif')
plt.show()
