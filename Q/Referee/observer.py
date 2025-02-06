from PySide6 import QtCore, QtWidgets, QtGui
from PIL.ImageQt import ImageQt
from PIL import Image, ImageDraw, ImageColor, ImageFont
import sys, os
import json
sys.path.insert(1, os.path.abspath('../Common'))
import encoder


'''
Graphical User Interface for the Observer. 
'''
class Renderer(QtWidgets.QMainWindow):
  def __init__(self):
    super(Renderer, self).__init__()
    self.buttons = {}
   
    self.title = "Grapical Display"
    self.setWindowTitle(self.title)

    self.layout = QtWidgets.QVBoxLayout()

    self.image = QtWidgets.QLabel(self)
    self.layout.addWidget(self.image)

    self.textbox = QtWidgets.QLineEdit(self)
    self.layout.addWidget(self.textbox)

    central_widget = QtWidgets.QWidget()
    central_widget.setLayout(self.layout)
    self.setCentralWidget(central_widget)

  '''
  Adds a clickable button to this layout that calls fn when clicked. 
  '''
  def create_button(self, name, fn): 
    button = QtWidgets.QPushButton(name)
    button.setEnabled(False)
    button.clicked.connect(fn)
    self.layout.addWidget(button)
    self.buttons[name] = button
  
  '''
  Updates this board image to the provided image.
  '''
  def update_board_image(self, board_image):
    self.image.setPixmap(QtGui.QPixmap.fromImage(ImageQt(board_image)))
    self.resize(self.image.width(), self.image.height())
    self.image.repaint()


'''
Observer_state_manager manages all the states that the observer has access to and will allow
the states to be traversed by calling next_state and previous_state. 
'''
class Observer_state_manager():
  def __init__(self):
    self._states = []
    self._current_state = 0

  '''
  Adds a state to the state manager.
  '''
  def add_state(self, state):
    self._states.append(state)
  
  '''
  Returns true if there is a state before the current state.
  '''
  def has_previous_state(self):
    return self._current_state > 0

  '''
  Update this to the previous state. Assumes a call to has_previous_state has 
  been made before a call to this method.
  '''
  def previous_state(self):
      self._current_state -= 1

  '''
  Returns true if there is a state after the current state.
  '''
  def has_next_state(self):
    return self._current_state in range(0, len(self._states) - 1)

  '''
  Update this to the next state. Assumes a call to has_next_state has 
  been made before a call to this method.
  '''
  def next_state(self):
      self._current_state += 1

  '''
  Returns true if the current state is not the beginning or ending screen.
  '''
  def has_current_state(self):
    return self._current_state in range(0, len(self._states))

  '''
  Gets the current state. 
  '''
  def get_current_state(self):
      return self._states[self._current_state]
  
  '''
  Returns true if the state is the beginning state.
  '''
  def is_beginning_state(self):
    return self._current_state == 0


class StartState():
  def __init__(self):
    self.im = Image.new("RGBA", (500, 500))
    draw = ImageDraw.Draw(self.im)
    font = ImageFont.truetype("../../Q/Common/Other/Arial.ttf", 30)
    draw.text((200, 240), "Beginning", fill="black", font=font)
    
  def render_state(self):
    return self.im

class EndState():
  def __init__(self):
    self.im = Image.new("RGBA", (500, 500))
    draw = ImageDraw.Draw(self.im)
    font = ImageFont.truetype("../../Q/Common/Other/Arial.ttf", 30)
    draw.text((200, 240), "Ending", fill="black", font=font)
    
  def render_state(self):
    return self.im

'''
Represents the observer that the Referee interacts with and sends states to.
'''
class Observer():
    def __init__(self):    
        self._states = Observer_state_manager()
        self.renderer = Renderer()

        self.next_button_name = "Next"
        self.previous_button_name = "Previous"
        self.save_button_name = "Save"

        self.renderer.create_button(self.next_button_name, self.next_state)
        self.renderer.create_button(self.previous_button_name, self.previous_state)
        self.renderer.create_button(self.save_button_name, self.save_state)
        self._states.add_state(StartState())

        self._update_image()

    '''
    
    '''
    def add_state(self, state):
        self._states.add_state(state)
        self.renderer.buttons[self.next_button_name].setEnabled(True)
        self.save_state_to_file(state)

    '''
    saves the given state from one of this states
    '''
    def save_state_to_file(self, state):
        state_image = state.render_state()
        if not os.path.exists("Tmp/"):
          os.makedirs("Tmp/")
        state_image.save("Tmp/" + str(self._states._states.index(state) - 1)+ ".png", format="PNG")
     
    '''
    When the referee has no more states to give
    '''
    def no_more_states(self):
      self._states.add_state(EndState())

    '''
    advances this current state to the next chronological one
    '''
    def next_state(self):
      if self._states.has_previous_state():
        self.renderer.buttons[self.previous_button_name].setEnabled(True)

      if self._states.has_next_state():
        self.renderer.buttons[self.save_button_name].setEnabled(True)
        self._states.next_state()
        self._update_image()
        if not self._states.has_next_state():
          self.renderer.buttons[self.next_button_name].setEnabled(False)
      else:
        self.renderer.buttons[self.next_button_name].setEnabled(False)

        
      if not self._states.is_beginning_state():
          self.renderer.buttons[self.save_button_name].setEnabled(True)
        

    '''
    advances this current state to the previous chronological one.
    '''
    def previous_state(self):
      if self._states.has_previous_state():
        self._states.previous_state()
        self._update_image()
        self.renderer.buttons[self.next_button_name].setEnabled(True)
      else:
        self.renderer.buttons[self.previous_button_name].setEnabled(False)
      if not self._states.has_previous_state():
          self.renderer.buttons[self.previous_button_name].setEnabled(False)
      if self._states.is_beginning_state():
        self.renderer.buttons[self.save_button_name].setEnabled(False)

    '''
    saves this current state
    '''
    def save_state(self):
      if self._states.has_current_state():
        json_state = encoder.serialize_jpub(self._states.get_current_state())
        with open(self.renderer.textbox.text(), "w") as outfile:
          outfile.write(json.dumps(json_state, separators=(',', ':')))

    '''
    updates this displayed image
    '''
    def _update_image(self):
      if self._states.has_current_state():
        state_image = self._states.get_current_state().render_state()
        self.renderer.update_board_image(state_image)
        