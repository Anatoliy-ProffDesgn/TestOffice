import turtle as t
# from turtle import *
s=t.speed()
t.setup(700, 700, 0, 0);t.speed(0)
t.penup(); t.setx(0);t.sety(-340)
t.pendown(); t.goto(0,340)
t.penup(); t.goto(-340,0)
t.pendown(); t.goto(340,0)
t.speed(s)
t.mainloop()


