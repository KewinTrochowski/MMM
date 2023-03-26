import math

k1 = 5
k2 = 5
m1 = 10
m2 = 10
b1 = 5

f = 1
A = 1
T = 100
Fs = 10000
phase_shift = 0


class Signals:
    def __init__(self, f, A, T, Fs, phase_shift=0):
        self.f = f
        self.A = A
        self.T = T
        self.Fs = Fs
        self.samples = []
        self.phase_shift = phase_shift

    def create_square_wave(self):
        N = self.Fs * self.T
        for i in range(N):
            t = i * 1 / Fs
            if t % (1 / f) < (1 / (f * 2)):
                self.samples.append(-A)
            else:
                self.samples.append(A)

    def create_sin_wave(self):
        N = self.Fs * self.T
        for i in range(N):
            t = i * 1 / Fs
            self.samples.append(math.sin(2 * math.pi * self.f * t + self.phase_shift))

    def create_triangle_wave(self):
        N = self.Fs // self.f // 4

        for i in range(self.f * self.T):
            for a in (1, -1):
                for j in range(N):
                    self.samples.append(j * (self.A / N) * a)
                for j in range(N):
                    self.samples.append((self.A - (j * (self.A / N))) * a)


def diff_eq1(x1, x2, x3, x4):
    return (k1 * (x2 - x1) + b1 * (x4 - x3)) / m1


def diff_eq2(x1, x2, x3, x4, u):
    return (k2 * (u - x2) + k1 * (x1 - x2) + b1 * (x3 - x4)) / m2


output1_tr = []
output2_tr = []
output1_sin = []
output2_sin = []
output1_sq = []
output2_sq = []

print('Tworzę sygnały...')
square = Signals(f, A, T, Fs)
square.create_square_wave()
sinus = Signals(f, A, T, Fs, phase_shift)
sinus.create_sin_wave()
triangle = Signals(f, A, T, Fs, phase_shift)
triangle.create_triangle_wave()

for j in range(3):
    x1 = 0
    x2 = 0
    x3 = 0
    x4 = 0
    u = 0
    dt = 1 / Fs
    for i in range(Fs * T):
        if j == 0:
            u = triangle.samples[i]
            output1_tr.append(x1)
            output2_tr.append(x2)
        elif j == 1:
            u = square.samples[i]
            output1_sq.append(x1)
            output2_sq.append(x2)
        elif j == 2:
            u = sinus.samples[i]
            output1_sin.append(x1)
            output2_sin.append(x2)

        x2 += dt * x4
        x1 += dt * x3
        x4 += dt * diff_eq2(x1, x2, x3, x4, u)
        x3 += dt * diff_eq1(x1, x2, x3, x4)

import matplotlib.pyplot as plt

time = []
for i in range(Fs * T):
    time.append(i * 1 / Fs)

fig, plot = plt.subplots(3)
print('Wpisz "1", aby wyświetlić wykresy położenia od czasu zmiennej "x".')
print('Wpisz "2", aby wyświetlić wykresy położenia od czasu zmiennej "y".')
print('Wpisz "3", aby wyświetlić wykrey sygnałów wejściowych.')

inp = input()
if inp == '1':
    plot[0].plot(time, output1_sq)
    plot[0].grid()
    plot[0].set_xlabel('Czas [s]')
    plot[0].set_ylabel('x [m]')
    plot[1].plot(time, output1_sin)
    plot[1].grid()
    plot[1].set_xlabel('Czas [s]')
    plot[1].set_ylabel('x [m]')
    plot[2].plot(time, output1_tr)
    plot[2].grid()
    plot[2].set_xlabel('Czas [s]')
    plot[2].set_ylabel('x [m]')
    fig.suptitle('Wykresy położenia od czasu zmiennej "x" kolejno dla pobudzeń sygnałem: prostokątnym, sinusoidalnym i trójkątnym ')
    plt.show()
elif inp == '2':
    plot[0].plot(time, output2_sq)
    plot[0].grid()
    plot[0].set_xlabel('Czas [s]')
    plot[0].set_ylabel('y [m]')
    plot[1].plot(time, output2_sin)
    plot[1].grid()
    plot[1].set_xlabel('Czas [s]')
    plot[1].set_ylabel('y [m]')
    plot[2].plot(time, output2_tr)
    plot[2].grid()
    plot[2].set_xlabel('Czas [s]')
    plot[2].set_ylabel('y [m]')
    fig.suptitle('Wykresy położenia od czasu zmiennej "y" kolejno dla pobudzeń sygnałem: prostokątnym, sinusoidalnym i trójkątnym')
    plt.show()
elif inp == '3':
    sq_buf = []
    sin_buf = []
    tr_buf = []
    time_buf = []
    for i in range(Fs):
        sq_buf.append(square.samples[i])
        sin_buf.append(sinus.samples[i])
        tr_buf.append(triangle.samples[i])
        time_buf.append(time[i])
    plot[0].plot(time_buf, sq_buf)
    plot[0].grid()
    plot[0].set_xlabel('Czas [s]')
    plot[0].set_ylabel('A [m]')
    plot[1].plot(time_buf, sin_buf)
    plot[1].grid()
    plot[1].set_xlabel('Czas [s]')
    plot[1].set_ylabel('A [m]')
    plot[2].plot(time_buf, tr_buf)
    plot[2].grid()
    fig.suptitle('Wykresy sygnałów wejściowych')
    plot[2].set_xlabel('Czas [s]')
    plot[2].set_ylabel('A [m]')
    plt.show()
