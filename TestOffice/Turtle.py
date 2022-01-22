import turtle as t
# from turtle import *
s = t.speed()
t.setup(740, 740, 0, 0);    t.speed(0)
t.screensize(bg = '#6897BB')

# Рисуем координатную сетку
x = -360; t.pencolor('#E7EAED')
while x < 340:
    x += 15
    if x == 0:
        continue
    t.penup();      t.setx(x);  t.sety(-340)
    t.pendown();    t.goto(x,340)
    t.penup();      t.setx(-340);  t.sety(x)
    t.pendown();    t.goto(340, x)
#t.setworldcoordinates(-340,-340,340,340)

t.pencolor('#2B2B2B')
# Рисуем оси координат
t.penup();      t.setx(0);  t.sety(-340)    # начало оси Y
t.pendown();    t.goto(0,340)               # конец оси Y
t.penup();      t.goto(-340,0)              # начало оси X
t.pendown();    t.goto(340,0)               # конец оси X

# Рисуем стрелочку Х
t.penup();      t.goto(340, 0)
t.pendown();    t.right(10);   t.fd(-15)
t.penup();      t.goto(340, 0)
t.pendown();    t.left(20);    t.fd(-15)
# Рисуем стрелочку У
t.penup();      t.goto(0, 340)
t.pendown();    t.right(270);   t.fd(-15)
t.penup();      t.goto(0, 340)
t.pendown();    t.right(20);    t.fd(-15)

t.speed(s); t.hideturtle()# t.penup();  t.goto(-340, -340)
t.mainloop()


