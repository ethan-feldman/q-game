import sys, os
import json
import map
import decoder
sys.path.insert(1, os.path.abspath('../Q/Referee'))
import referee
import observer
from PySide6 import QtCore, QtWidgets, QtGui


#reads the json import from standard in
def read_stdin_json():
    raw_input = ""
    while True:
        raw_input += input()
        try:
            json_input = json.loads(raw_input)
            return json_input
        except:
            pass

#the entrypoint function
def main():
    observer_list = []
    if "-show" in sys.argv:
        app = QtWidgets.QApplication(sys.argv)
        obs = observer.Observer()
        
    jstate = read_stdin_json()
    jactors = read_stdin_json()
    
    game_state = decoder.deserialize_jstate(jstate)
    players = decoder.deserialize_jactors(jactors)
    game_state.connect_remote_players(players)
    ref = referee.Referee(players, game_state)
    ref.attach(obs)


    winners, cheaters = ref.run_game_and_return_winners()
    winners.sort()

    output = []
    output.append(winners)
    output.append(cheaters)
    sys.stdout.write(json.dumps(output))

    if "-show" in sys.argv:
        window = obs.renderer
        window.show()
        app.exec()

if __name__ == '__main__':
    main()