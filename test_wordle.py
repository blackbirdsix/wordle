from colorama import Fore
from IPython.display import clear_output
import pytest
from unittest.mock import Mock, patch

import wordle

# unfortunately i need to instantiate the class outside the function or else
# it reinstantiates every time the function is called, which would keep
# resetting the statistics, ruining the test_summary asserts
game = wordle.Wordle()
def mock_new_game(correct, a, b=None, c=None, d=None, e=None, f=None, g=None):
    """Used to simulate a user continually inputting answers. Used for tests.
    
       Parameters:
       -----------
       correct: str
           - the word that will be used as the correct word in the simulated game
       a: str
           - a five letter word to input
       b-g: str
           - all optional, same criteria as a"""
    # I learned how to mock multiple inputs from this forum:
    # https://stackoverflow.com/questions/66222805/mock-patch-multiple-user-inputs-in-sequence

    input_mock_change = Mock()  # First mock for changing correct word
    input_mock_change.return_value = 'change'

    input_mock_correct = Mock()  # Second mock for setting correct word
    input_mock_correct.return_value = correct

    input_mock_a = Mock()  # Third mock for first input
    input_mock_a.return_value = a

    input_mock_b = Mock()  # Fourth mock for second input
    input_mock_b.return_value = b

    input_mock_c = Mock()  # Fifth mock for third input
    input_mock_c.return_value = c

    input_mock_d = Mock()  # Sixth mock for fourth input
    input_mock_d.return_value = d

    input_mock_e = Mock()  # seventh mock for fifth input
    input_mock_e.return_value = e

    input_mock_f = Mock()  # eighth mock for sixth input
    input_mock_f.return_value = f
    
    input_mock_g = Mock()  # ninth mock for seventh input
    input_mock_g.return_value = g

    input_mock = Mock()    # Combine the mocks in another mock to patch the input call.
    input_mock.side_effect = [input_mock_change.return_value, input_mock_correct.return_value,
                              input_mock_a.return_value, input_mock_b.return_value,
                              input_mock_c.return_value, input_mock_d.return_value,
                              input_mock_e.return_value, input_mock_f.return_value,
                             input_mock_g.return_value]
    with patch('builtins.input', input_mock) as mock_input:
        game.new_game()
    return game

def check_list(string, color):
    """Used in test_new_game to check that all letters light up when it's either correct, or all
       the letters are in the word but the wrong position.
       
       Parameters:
       -----------
       string: str
           - a five letter string to check
       color: str
           - a color to match to
           
       Returns:
       colored_list: list
           - a list containing each letter as the selected color"""
    colored_list = []
    for char in string:
        colored_list.append(color + char.upper() + Fore.BLACK)
    return colored_list

def test_new_game():
    assert callable(wordle.Wordle.new_game)
    
    # checks that words are capitalized
    assert (mock_new_game('Phyla', 'poppy', 'phyla').correct_word == 
            (mock_new_game('Phyla', 'poppy', 'phyla').correct_word).upper())
    assert (mock_new_game('Phyla', 'poppy', 'phyla').used_words[0] == 'POPPY')
    assert (mock_new_game('PHYLA', 'POPPY', 'phyla').used_words[0] == 'POPPY')
    assert (mock_new_game('phyla', 'poPpy', 'phyLA').used_words[0] == 'POPPY')

    
    # checks that inputs are working correctly 
        # 'stop' stops the loop
    assert mock_new_game('Phyla', 'stop').grid_list[0][0] == '.'
    assert mock_new_game('phyla', 'poppy', 'phyla').correct_word == 'PHYLA'
        # five letter words don't work
    assert (mock_new_game('phyla', 'this is not a five letter word', 'poppy', 'phyla').used_words[0]
            == 'POPPY')
        # non letters don't work
    assert '!' not in mock_new_game('phyla', '!3425', 'poppy', 'phyla').used_words
        # repeat words don't work
    assert mock_new_game('phyla', 'poppy', 'poppy', 'phyla').used_words[1] == 'PHYLA'
        # only real words (in the provided list)
    assert mock_new_game('phyla', 'glorf', 'poppy', 'phyla').used_words[0] == 'POPPY'
        # blanks don't work
    assert (mock_new_game('Phyla', '', 'stark', 'train', 'blast', 'plate', 'poppy', 'phyla')
            .used_words[5] == 'PHYLA')
        # only six inputs are possible
    assert (len(mock_new_game('Phyla', 'crate', 'stark', 'train', 'blast', 'plate', 'poppy', 'phyla')
           .used_words) == 6)
    
    # checks that the letters are lighting up where they should
    assert mock_new_game('Phyla', 'poppy', 'phyla').grid_list[0][0] == (Fore.GREEN + "P" + Fore.BLACK)
    assert mock_new_game('Phyla', 'poppy', 'phyla').grid_list[0][4] == (Fore.YELLOW + "Y" + Fore.BLACK)
    assert (mock_new_game('Phyla', 'poppy', 'ocean', 'phyla').grid_list[1][2] == "E")
    
    # checks for double occurences of colors when there should only be one of the same letter
    # simultaneously checks that the letters/colors are in the right position when list is full
    # when guessed count letter > actual count letter
        # 1 green before and 2 grays after
    assert ((
        mock_new_game('Phyla', 'stark', 'train', 'blast', 'plate', 'poppy', 'phyla').grid_list[4][2] and 
        mock_new_game('Phyla', 'stark', 'train', 'blast', 'plate', 'poppy', 'phyla').grid_list[4][3])
        == ("P"))
        # 1 green before and 1 gray after
    assert (mock_new_game('Phyla', 'stark', 'train', 'blast',
                          'plate', 'piper', 'phyla').grid_list[4][2] == "P")
    assert (mock_new_game('Phyla', 'stark', 'train', 'blast',
                          'plate', 'piper', 'phyla').grid_list[4][0] == (Fore.GREEN + "P" + Fore.BLACK))
        # 1 gray before 1 green after
    assert mock_new_game('shore', 'stark', 'train', 'blast',
                          'plate','breve', 'shore').grid_list[4][2] == "E"
    assert mock_new_game('shore', 'stark', 'train', 'blast',
                          'plate','breve', 'shore').grid_list[4][4] == (Fore.GREEN + "E" + Fore.BLACK)
    
    # checks the scenario they're all yellow
    assert mock_new_game('glean', 'angle', 'glean').grid_list[0] == check_list('angle', Fore.YELLOW)
    # checks the scenario they're all green
    assert mock_new_game('glean', 'glean').grid_list[0] == check_list('glean', Fore.GREEN)

def test_summary():
    #there are 21 asserts with 1 instance and 1 with 2 (the 'and' assert)
    assert callable(game.summary)
    assert len(game.total_record) == 23
    assert game.win_streak == 11
    assert game.highest_win_streak == 11
    game.summary()
    clear_output()
    assert game.win_percent == round(22/23 * 100)
    
def test_clear_statistics():
    assert game.total_tries == [1, 13, 1, 0, 0, 7]
    assert len(game.total_record) == 23
    game.clear_statistics()
    assert game.total_tries == [0, 0, 0, 0, 0, 0]
    assert len(game.total_record) == 0
    assert game.win_streak == 0
    assert game.highest_win_streak == 0
    assert game.win_percent == None