import turtle as t
t.forward(10) #   вперед на 10
t.fd(10)      #   вперед на 10
t.bk(100)     #   назад на 100
t.fd(-100)    #   назад на 100
t.right(90)   #   повернуть направо на 90 градусов
t.rt(90)      #   повернуть направо на 90 градусов
t.lt(-90)     #   повернуть направо на 90 градусов
t.lt(90)      #   повернуть налево на 90 градусов
t.left(90)    #   повернуть налево на 90 градусов
t.rt(-90)             #   повернуть налево на 90 градусов
t.setpos(-100,100)    #   переместить Черепашку в точку -100,100 (центр экрана — это точка 0,0)
t.goto(-100,100)      #   переместить Черепашку в точку -100,100 (центр экрана — это точка 0,0)
t.x,y = t.pos()         #   узнать координаты Черепашки
t.begin_fill()        #   начать закрашенную фигуру
t.end_fill()          #   закончить закрашенную фигуру
t.color ('lightgreen') #  изменить цвет
t.color ('red','blue') #  изменить цвета линий и заливки
t.circle(40)  #   рисовать окружность радиусом 40
t.home()      #   вернуться в начальную точку в центре экрана, голова – направо
t.dot()       #   нарисовать точку
t.speed(1)    #   Установить самую низкую скорость
t.speed(6)    #   Значение скорости по умолчанию
t.speed(10)   #   Установить самую высокую скорость
t.speed(0)    #   Установить самую высокую скорость
t.pd()        #   опустить перо (будет оставлять след)
t.pendown()   #   опустить перо (будет оставлять след)
t.down()      #   опустить перо (будет оставлять след)
t.pu()        #   поднять перо (не будет оставлять след)
t.penup()     #   поднять перо (не будет оставлять след)
t.up()        #   поднять перо (не будет оставлять след)
t.st()        #   показать черепашку
t.showturtle()    #  показать черепашку
t.ht()            #   спрятать черепашку
t.hideturtle()    #   спрятать черепашку
t.setup (500,500) #   Установить размеры экрана
t.mainloop()      #   Не закрывать окно
for i in range () #цикл ( повторення)

