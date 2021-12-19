"""
COMP3005 FALL21
ERIC JONES 101113060

The purpose of this module is to provide
a sturdy framework for the program to run off of.
provides basis for all command-based input in this
program
"""
from os import system
import re

"""
Executor:
    handles command-based input. Used frequently
    throughout the program
"""
class Executor:

    def __init__(self):
        #this variable will hold all commands the user can execute
        self.functions = {}

    """
    add_command:
        adds another regex to check for on an input.
        if the input matches the regex, then the command is executed
    inputs:
        regex: regular expression that represents the users input
        command: the function/method to be executed on success
        description: description of the command
    """
    def add_command(self, regex: str, command, command_name: str, description: str):
        #insert the new command to the dictionary
        self.functions[regex] = [command, command_name, description]

    """
    remove_command:
        removes the command from the list if it exists
    inputs:
        key:the re expression used on the command
    returns: if the command was successfully deleted
    """
    def remove_command(self, key: str) -> bool:
        
        #if the key is a valid key, delete the command
        contained = key in self.functions.keys()
        if contained:
            del self.functions[key]

        return contained

    """
    start:
        starts the execution loop.
    """
    def start(self):
        #loop until broken
        while True:

            #clear the screen
            system('cls')
            
            #run any pre-calculations/prints necessary
            self.preamble()

            #print each command option with description
            for value in self.functions.values():
                print(value[1] + ": " + value[2])

            
            command = None
            #wait for a valid command
            while command is None:
                #get user input
                called_command = input().lower()

                #get the first match
                try:
                    command = next(x for x in self.functions.keys() if re.match(x,called_command))
                except:
                    #if no match found, continue the loop
                    print("Command not found. Please try again.")

            #get the command
            cmd = self.functions[command][0]
            #execute (with user input as a parameter), if returned True end the loop
            if cmd(called_command):
                break

    """
    preamble:
        used abstract here, preamble is intended to run
        any pre-computations (and more notably, print statements)
        before printing the list of commands.
    """
    def preamble(self):
        pass

"""
Program:
    inherited by Executor, Program simply adds the functionality
    of exiting the program, and providing an initial prompt in the
    preamble
"""
class Program(Executor):

    def __init__(self):
        super().__init__()
        #add the exit command
        self.add_command("exit", self.quit, "exit", "Exits the program")

    """
    preamble:
        [OVERRIDE]
        adds initial prompt to command
    """
    def preamble(self):
        print("What would you like to do?")
        print("--------------------------")

    """
    quit:
        closes the program
    """
    def quit(self, param):
        confirm_exit = input("Are you sure you want to exit? [y/n]")
        if confirm_exit.lower() == 'y':
            exit()

if __name__ == "__main__":
    pgm = Program()
    pgm.start()
