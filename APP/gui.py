from random import choice

from kivy.app import App
from kivy.core.window import Window

from kivy.clock import Clock

from kivy.graphics import  Line, Color, Ellipse
from kivy.uix.widget import Widget

class Any_Object():
    """класс возвращает координаты некоторых объектов
    для удобства отрисовки схемы паркови"""
    def __init__(self):
        self.width = 40
        self.lenght = 60
    def row_with_open_bottom(self, cnt_of_places, x=0, y=0):
        '''генерирует ряд с открытым низом'''
        list_of_cords_for_lines = [x, y]
        list_of_cords_for_ellipses=[(x + self.width // 2, y + self.lenght // 2)]
        for _ in range(cnt_of_places):

            list_of_cords_for_lines += [
                x, y+self.lenght,
                x+self.width, y+self.lenght,
                x+self.width, y
            ]

            x+=self.width

            list_of_cords_for_ellipses += [(
                x+self.width//2,
                y+self.lenght//2
            )]
        return list_of_cords_for_lines, list_of_cords_for_ellipses[:-1]
    def row_with_open_up(self, cnt_of_places, x=0, y=0):
        '''генерирует ряд с открытым верхом'''
        list_of_cords_for_lines = [x, y]

        list_of_cords_for_ellipses=[(
            x + self.width // 2,
            y + self.lenght // 2
        )]

        for _ in range(cnt_of_places):

            list_of_cords_for_lines += [
                x, y+self.lenght,
                x, y,
                x+self.width, y
            ]
            x+=self.width

            list_of_cords_for_ellipses += [(
                x + self.width // 2,
                y + self.lenght // 2
            )]

        else:
            list_of_cords_for_lines+=[
                x,
                y+self.lenght
            ]
        return list_of_cords_for_lines, list_of_cords_for_ellipses[:-1]

class MyWidget(Widget):
    def __init__(self, **kwargs):
        super(MyWidget, self).__init__(**kwargs)

        with self.canvas:
            Color(0.5, 0.5, 0.5)

            self.cords_of_open_down_row = Any_Object().row_with_open_bottom(12, 140, 300)
            self.cords_of_open_up_row = Any_Object().row_with_open_up(12, 140, 200)

            Line(points=self.cords_of_open_down_row[0])
            Line(points=self.cords_of_open_up_row[0])

            Color(0, 1, 0)
            for i in self.cords_of_open_down_row[1]:
                Ellipse(pos=i, size=(10, 10))
            for i in self.cords_of_open_up_row[1]:
                Ellipse(pos=i, size=(10, 10))

###########хуйня для теста#######
            Color(1, 0, 0)#

            Clock.schedule_once(self.update, 1)#
            Clock.schedule_once(self.update, 2)  #
            Clock.schedule_once(self.update, 3)  #
            Clock.schedule_once(self.update, 4)  #
    def update(self, dt):#
        with self.canvas:#
            Ellipse(pos=choice(self.cords_of_open_down_row[1]+self.cords_of_open_up_row[1]), size=(10, 10))#
###########хуйня для теста

class ParkingApp(App):
    def build(self):
        Window.clearcolor = (0, 0, 0, 0)#смена заднего фона
        return MyWidget()

if __name__ == '__main__':
    t = ParkingApp()
    t.run()

