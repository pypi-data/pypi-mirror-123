from math import *


# basic arithmetic operations
def add(num1, num2):
    print(num1 + num2)


def multiply(num1, num2):
    print(num1 * num2)


def divide(num1, num2):
    print(num1 / num2)


def sub(num1, num2):
    print(num1 - num2)

# exponential operators
# smol note: Don't use negative numbers! (only for cuberoot)


def root(num):
    print(sqrt(num))


def sqr(num):
    print(num * num)


def cube(num):
    print(num * num * num)


def cuberoot(num):
    print(num ** 1 / 3)

# trignometry operators
# Take approx. because the conversion is 80% accurate!!!


def sine(num1):
    print(sin(num1 * 0.017453))


def cosine(num):
    print(cos(num * 0.017453))


def tangent(num):
    print(tan(num * 0.017453))


# trignometric square calculators

def sinsqr(num):
    a = sin(num * 0.017453)
    b = a * a
    print(b)


def cossqr(num):
    a = cos(num * 0.017453)
    b = a ** 2
    print(b)


def tansqr(num):
    a = tan(num * 0.017453)
    b = a ** 2
    print(b)

def radsin(num):
    print(sin(num))


def radcos(num):
    print(cos(num))

def radtan(num):
    print(tan(num))


def radsinsqr(num):
    a = sin(num)
    b = a ** 2
    print(b)


def radcossqr(num):
    a = cos(num)
    b = a ** 2


def radtansqr(num):
    a = tan(num)
    b = a ** 2


def triangle(angle1, angle2):
    missingangle = 180 - (angle1 + angle2)
    print(missingangle)

def quadrilateral(angle1, angle2, angle3):
    missingangle = 360 - (angle1 + angle2 + angle3)
    print(missingangle)

def pentagon(angle1, angle2, angle3, angle4):
    missingangle = 540 - (angle1 + angle2 + angle3 + angle4)
    print(missingangle)

def hexagon (angle1, angle2, angle3, angle4, angle5):
    missingangle = 720 - (angle1 + angle2 + angle3 + angle4 + angle5)
    print(missingangle)

def comp(angle):
    a = 90 - angle
    print(a)

def supp(angle):
    a = 180 - angle
    print(a)


def typeofangle(angle):
    if angle == 180:
        print(str(angle) + ' Straight angle')

    elif angle == 90:
        print(str(angle) + ' Right angle')

    elif angle == 360:
        print(str(angle) + ' Complete angle')

    elif angle == 0:
        print(str(angle) + ' No angle is formed!')

    elif angle > 90 and angle <180:
        print(str(angle) + ' Obtuse angle')
   
    elif angle < 90:
        print(str(angle) + ' Acute angle')

    elif angle > 180 and angle <360:
        print(str(angle) + ' Reflex angle')

    elif angle > 360:
        print('Please enter a valid angle!')

    else:
        pass

def areasqr(side):
    a = str(input('(c)m or (m): '))
    if a == 'c':
        n = side * side
        print(str(n) + ' cm^2')

    elif a == 'm':
        n = side ** 2
        print (str(n) + ' m^2')

    else:
        print('Please enter a valid input! ')

def arearect(length, breadth):
    a = str(input('(c)m or (m): '))
    if a == 'c':
        n = length * breadth
        print(str(n) + ' cm^2')

    elif a == 'm':
        n = length * breadth
        print(str(n) + ' m^2')

    else:
        print('Please enter a valid input! ')

def areacircle(radius):
    a = str(input('(c)m or (m): '))
    if a == 'm':
        n = 3.142857142857 * (radius ** 2)
        print(str(n) + ' m^2')

    elif a == 'c':
        n = 3.142857142857 * (radius ** 2)
        print(str(n) + ' cm^2')

    else:
        print('Please enter a valid input! ')

def areaparellelogram(length, height):
    a = str(input('(c)m or (m): '))
    if a == 'c':
        n = length * height
        print(str(n) + ' cm^2')

    elif a == 'm':
        n = length * height
        print(str(n) + ' m^2')

    else:
        print('Please enter a valid input! ')

def areatrapezium(parallelside1, parallelside2, height):
    a = str(input('(c)m or (m): '))
    if a == 'c':
        n = 0.5 * (parallelside1 + parallelside2) * height
        print(str(n) + ' cm^2')

    elif a == 'm':
        n = 0.5 * (parallelside1 + parallelside2) * height
        print(str(n) + ' m^2')

    else:
        print('Please enter a valid input! ')

def persqr(side):
    a = str(input('(c)m or (m): '))
    if a == 'c':
        n = 4 * side
        print(str(n) + ' cm')

    elif a == 'm':
        n = 4 * side
        print(str(n) + ' m')

    else:
        print('Please enter a valid input! ')

def perrect(length, breadth):
    a = str(input('(c)m or (m): '))
    if a == 'c':
        n = 2 * (length + breadth)
        print(str(n) + ' cm')

    elif a == 'm':
        n = 2 * (length + breadth)
        print(str(n) + ' m')

    else:
        print('Please enter a valid input! ')
