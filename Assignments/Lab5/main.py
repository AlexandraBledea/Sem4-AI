from controller import Controller
from gui import GUI

if __name__ == '__main__':
    controller = Controller()
    gui = GUI(controller)
    gui.start()
