from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.config import Config

import snakeGame as Game


class MyApp(App):
    def build(self):
        return MyGrid()

'''
function to start the game as Ai using A start algorithm
'''
def a_star_play(instance):
    Game.start_game("a_star")

'''
function to start the game as Ai using Q learning machine
'''
def q_learing_play(instance):
    Game.start_game("q_learning")

'''
function to start the game as Ai using Q learning machine
'''
def bfs_play(instance):
    Game.start_game("bfs")

'''
function to start the game as user play
'''
def human_play(instance):
    Game.start_game("human")

'''
layout grid with define buttons to activate functions
'''
class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.cols = 1

        self.insideTemplete = GridLayout()
        self.insideTemplete.cols = 1

        self.submit = Button(text="Play", font_size=40)
        self.submit.bind(on_press=human_play)
        self.add_widget(self.submit)

        self.submit = Button(text="AI-Astar play", font_size=40)
        self.submit.bind(on_press=a_star_play)
        self.add_widget(self.submit)

        self.submit = Button(text="AI-Qlearning play", font_size=40)
        self.submit.bind(on_press=q_learing_play)
        self.add_widget(self.submit)

        self.submit = Button(text="BFS play", font_size=40)
        self.submit.bind(on_press=bfs_play)
        self.add_widget(self.submit)

        self.submit = Button(text="AI-IDAstar play", font_size=40)
        self.submit.bind(on_press=bfs_play)
        self.add_widget(self.submit)
        # ------------------------------------------------------



if __name__ == "__main__":
    global database
    Config.set('graphics', 'width', '600')
    Config.set('graphics', 'height', '600')
    MyApp().run()
    # for _ in range(10):
    #     Game.start_game("bfs")
