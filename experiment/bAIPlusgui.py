"""
Quick script to register babyAI++ levels before passing to babyAI gui.
"""

import sys
import os
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(),"babyai/scripts"))
import babyaiPP
import gui

if __name__ == '__main__':
    gui.main(sys.argv)
