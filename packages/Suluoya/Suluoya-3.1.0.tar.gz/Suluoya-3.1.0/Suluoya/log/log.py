import os
from time import asctime, localtime, time
from random import choice

import pretty_errors
from termcolor import colored





def hide():
    print(f'\033[0;30;40m',end='')

def show():
    print(colored('', 'white'), end='')


def sprint(content, color=False):
    '''Color Output
    '''
    color_list = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan']
    if not color:
        print(colored(content, color=choice(color_list)))
    else:
        print(colored(content, color=color))


class slog(object):
    def __init__(self, filename='Suluoya'):
        try:
            os.makedirs('./slog')
        except:
            pass
        self.filename = filename
        with open(f'slog\\{self.filename}.log', 'w', encoding='utf8') as f:
            f.write(asctime(localtime(time()))+'\n')
            f.write("(｡･∀･)ﾉﾞ嗨!\n\n")

    def log(self, content='Suluoya', mode=0):
        '''
        Logs a message
        0:\\n{content}\\n
        1:\\n{content}
        2:  {content }  
        '''
        mode_dict = {0: f'\n{content}\n',
                     1: f'\n{content}',
                     2: f'{content} '}
        with open(f'slog\\{self.filename}.log', 'a', encoding='utf8') as f:
            f.write(mode_dict[mode])


if __name__ == '__main__':
    sprint('Suluoya')
    slog = slog(filename='Suluoya')
    slog.log('se', 2)
