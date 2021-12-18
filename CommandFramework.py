from os import system
import re

class Executor:

    def __init__(self):
        self.functions = {}

    def add_command(self, regex, command, trigger_displayed, description):
        self.functions[regex] = [command, trigger_displayed, description]

    def remove_command(self, key):
        contained = key in self.functions.keys()
        if contained:
            del self.functions[key]

        return contained

    def start(self):

        while True:
            system('cls')
            self.preamble()
            for value in self.functions.values():
                print(value[1] + ": " + value[2])

            
            command = None
            while command is None:
                called_command = input().lower()
                try:
                    command = next(x for x in self.functions.keys() if re.match(x,called_command))
                except:
                    print("Command not found. Please try again.")
                    called_command = input().lower()

            cmd = self.functions[command][0]
            if cmd(called_command):
                break
    
    def preamble(self):
        pass

class Program(Executor):

    def __init__(self):
        super().__init__()
        self.add_command("exit", self.quit, "exit", "Exits the program")

    def preamble(self):
        print("What would you like to do?")
        print("--------------------------")

    def quit(self, param):
        confirm_exit = input("Are you sure you want to exit? [y/n]")
        if confirm_exit.lower() == 'y':
            exit()

if __name__ == "__main__":
    pgm = Program()
    pgm.start()
