import random

import pandas as pd
from IPython.display import clear_output

from colorama import Fore

class Wordle():
    
    # creates the grid for the game and the word bank
    # source of word bank: https://www-cs-faculty.stanford.edu/~knuth/sgb-words.txt
    word_bank = open("five_letter_words.txt").read().split() 
    
    # got this line from A4 part III
    # modified for my own code
    grid_list = [['.'] * 5 for ncols in range(6)]
    
    def __init__(self, row=0, column=0):
        """Instantiates the base values used in the class
        """
        
        self.row = 0
        self.column = 0
        self.correct_word = random.choice(self.word_bank).upper()
        self.letter_index = 0
        self.correct_answer = False
        self.total_record = []
        self.number_of_tries = 0
        self.total_tries = [0, 0, 0, 0, 0, 0]
        self.possible_tries = [1, 2, 3, 4, 5, 6]
        self.win_streak = 0
        self.highest_win_streak = 0
        self.win_percent = None
        
    def new_game(self):
        """Starts a new game of Wordle.
        
        Parameters
        ----------
        self
        
        Returns
        -------
        - continuous input lines
        - printed colored grids of input words
        - when user fails to win, the correct answer
        """
        self.grid_list = [['.'] * 5 for ncols in range(6)]
        self.row = 0
        self.column = 0
        self.correct_word = random.choice(self.word_bank).upper()
        self.letter_index = 0
        self.number_of_tries = 0
        self.correct_answer = False
        self.used_words = []
        self.change_position = 0
        self.previous_index = 10 #arbitrary number
        self.green_list = []
        self.letters_in_word = []
        self.yellow_list = []
        self.keyboard = "\nQ W E R T Y U I O P \n A S D F G H J K L \n  Z X C V B N M"
        
        
        if self.used_words == []:
                print("Enter 'stop' to quit the game.")
        
        # adds each letter to a list, used to
        # ensure correct # of green and yellow letters
        for letter in self.correct_word:
            self.letters_in_word.append(letter)

        
        # loop that keeps asking for an input
        # until user either reaches the max number
        # of guesses (6), they guess the correct
        # answer, or they input the termination commnad
        while self.correct_answer == False:
            self.yellow_list = []
            self.green_list = []
            
            word = input('Your word:\t')
            
            # stops function
                
                
            if word == 'correct answer':
                print(self.correct_word)
            
            
            if word == 'change':
                self.correct_word = input('New word:\t').upper()
                self.letters_in_word = []
                for letter in self.correct_word:
                    self.letters_in_word.append(letter)
                word = input('Your word:\t')
            
            
            if word in ['stop', 'Stop', 'STOP']:
                break
            
            
            # raises error if word is not 5 letters
            try:
                if len(word) != 5:
                    raise
            except:
                print("Your word is not 5 letters long.")
                continue
            
            
            # raises error if nonletter in input
            try:
                for nonletter in '1234567890!@#$%^&*( [)]./;<>?:""}{+_-=':
                    if nonletter in word:
                        raise
            except:
                print('Your word must consist only of letters.')
                continue
           
        
            # capitalizes all of input
            word = word.upper()
        
            
            # doesn't allow repeat words
            try:
                if word in self.used_words:
                    raise
            except:
                print("You've already used this word.")
                continue        
            
            
            # makes sure the word is a real word
            # (according to the word bank at least)
            try:
                if word.lower() not in self.word_bank:
                    raise
            except:
                print("This is not a word.")
                continue 
            
            # when all above tests are passed,
            # the word is added to the used words
            self.used_words.append(word)
            
            
            # checks every letter in the word to determine what color it should print as and after
            # each loop it moves to the next position in the grid
            for letter in word:
                
                
                # prints letter green
                if letter == self.correct_word[self.letter_index]:
                    self.grid_list[self.row][self.column] = (Fore.GREEN + letter + Fore.BLACK)
                    # https://stackoverflow.com/questions/70263910/colorama-wont-stop-printing-colored-text
                    # learned from @SomeoneAlt86 how to stop printing in color

                    # (A1) if there are two occurences of a letter in guessed word and
                    # the second occurence is correct, makes sure previous ocurrence
                    # is black (as opposed to misleading yellow color). Refer to A2
                    # for second half of code.
                    if ((word.count(letter) > self.correct_word.count(letter)) and 
                        (self.letter_index > self.previous_index)):
                        self.grid_list[self.row][previous_column] = letter
                    
                    self.keyboard = self.keyboard.replace(letter, Fore.GREEN + letter + Fore.BLACK)
                    self.column += 1
                    self.letter_index += 1
                    self.green_list.append(letter)

                    
                # prints letter yellow    
                elif letter in self.correct_word:
                    
                    
                    if word.count(letter) <= self.correct_word.count(letter):
                        self.grid_list[self.row][self.column] = (Fore.YELLOW + letter + Fore.BLACK)

                        self.column += 1
                        self.letter_index += 1
                        
                    # makes sure that there are the correct number of yellow letters   
                    elif word.count(letter) > self.correct_word.count(letter):
                        
                        self.grid_list[self.row][self.column] = (Fore.YELLOW + letter + Fore.BLACK)
                        
                        if self.green_list.count(letter) == self.letters_in_word.count(letter):
                            self.grid_list[self.row][self.column] = letter
                        
                        
                        elif self.yellow_list.count(letter) == self.letters_in_word.count(letter):
                            self.grid_list[self.row][self.column] = letter
                        

                        self.yellow_list.append(letter)
                        
                        self.column += 1
                        self.letter_index += 1
                        # (A2) records position of yellow letter in grid to be
                        # overwritten as black if it needs to be
                        previous_column = self.column - 1
                        self.previous_index = self.letter_index - 1
    
                    self.keyboard = self.keyboard.replace(letter, (Fore.YELLOW + letter + Fore.BLACK))

                        
                # prints letter black
                elif letter not in self.correct_word:
                    self.grid_list[self.row][self.column] = letter

                    self.keyboard = self.keyboard.replace(letter, (Fore.WHITE + letter + Fore.BLACK))

                    self.column += 1
                    self.letter_index += 1

                    
                # moves on to the start of the next row (guess)    
                if self.column == 5:
                        self.column = 0
                        self.row +=1
                
                
                # lets code begin at first
                # letter of the new word
                if self.letter_index == 5:
                    self.letter_index = 0
                    
                    
            # got this line from A4 Part III  
            # clears each previous printed grid
            clear_output(wait=True)
            
            self.number_of_tries += 1
            
            # got this line from A4 part III
            # prints made grid
            print('\n'.join([' '.join(lst) for lst in self.grid_list]))

            print(self.keyboard)
            
            # depending on how many tries it took to guess the correct word, one count
            # is added to the respective position of [1, 2, 3 ,4, 5, 6]; used for
            # the graph in self.summary()
            if word == self.correct_word:
                
                # adds the tries it took them to guess to a list
                # containing all previous attempts
                self.total_record.append(self.number_of_tries)
                
                
                if self.number_of_tries == 1:
                    self.total_tries = [sum(i) for i in zip(self.total_tries,[1, 0, 0, 0, 0, 0])]
                    print("Wow! You solved the Wordle in " + str(self.number_of_tries) + ' try!')
                    
                    
                elif self.number_of_tries == 2:
                    self.total_tries = [sum(i) for i in zip(self.total_tries,[0, 1, 0, 0, 0, 0])]
                    print("You solved the Wordle in " + str(self.number_of_tries) + ' tries!')
                    
                    
                elif self.number_of_tries == 3:
                    self.total_tries = [sum(i) for i in zip(self.total_tries,[0, 0, 1, 0, 0, 0])]
                    print("You solved the Wordle in " + str(self.number_of_tries) + ' tries!')
                    
                    
                elif self.number_of_tries == 4:
                    self.total_tries = [sum(i) for i in zip(self.total_tries,[0, 0, 0, 1, 0, 0])]
                    print("You solved the Wordle in " + str(self.number_of_tries) + ' tries!')
                    
                    
                elif self.number_of_tries == 5:
                    self.total_tries = [sum(i) for i in zip(self.total_tries,[0, 0, 0, 0, 1, 0])]
                    print("You solved the Wordle in " + str(self.number_of_tries) + ' tries!')
                    
                    
                elif self.number_of_tries == 6:
                    self.total_tries = [sum(i) for i in zip(self.total_tries,[0, 0, 0, 0, 0, 1])]
                    print("You solved the Wordle in " + str(self.number_of_tries) + ' tries!')
                    
                    
                # increases tally for winstreak    
                if (self.win_streak == 0) or (self.total_record[-1] > 0):
                    self.win_streak +=1
                    
                    # updates highest win streak
                    if self.win_streak > self.highest_win_streak:
                        self.highest_win_streak = self.win_streak
                    
                # ends loop    
                self.correct_answer = True
            
            
            # When wordle is failed:
            if (self.number_of_tries == 6) and (word != self.correct_word):
            
                self.number_of_tries = 0
                
                
                # resets win streak
                if self.win_streak > 0:
                    self.win_streak = 0
                
                
                # adds failed attempt to list of attempts and ends loop
                self.total_record.append(self.number_of_tries)
                print(("The correct word was " + str(self.correct_word) + ". Better luck next time!"))
                self.correct_answer = True
                
    # resets all statistics, functionally the same as reinstantiating the class        
    def clear_statistics(self):
        """clears all statistics
        
        Parameters
        ----------
        self
        
        Returns
        -------
        none
        """
        self.total_record = []
        self.total_tries = [0, 0, 0, 0, 0, 0]
        self.win_streak = 0
        self.highest_win_streak = 0
        self.win_percent = None
        
    # returns a graph of all games played and printed statistics
    def summary(self):
        """Displays summary of cumulative games
        
        Parameters
        ----------
        self
        
        Returns
        -------
        - printed:
            - number of games played
            - win percent
            - current streak
            - highest streak
        - A graph of cumulative win counts
        """
        
        # prevents an error when there are no games yet
        try:
            if len(self.total_record) == 0:
                raise
        except:
            print('There are no statistics to print.')
            return
        
        # organizes statistical data from previously played games
        times_played = len(self.total_record)
        self.win_percent = round((sum(self.total_tries) / len(self.total_record)) * 100)
        current_streak = self.win_streak
        best_streak = self.highest_win_streak
        
        # creates dataframe and a graph based on it
        df_records = pd.DataFrame(self.total_tries, self.possible_tries,columns=['Tries'])
        df_records.columns = ['amount']
        tries_and_n_tries = df_records.reset_index()
        tries_and_n_tries.columns = ['Tries', 'amount']
        tries_and_n_tries.plot(kind='bar', y='amount', x='Tries');
        
        #prints statistical data
        print("Played:\t\t" + str(times_played))
        print("Win percent:\t" + str(self.win_percent) + "%")
        print("Current streak:\t" + str(current_streak))
        print("Best streak:\t" + str(best_streak))