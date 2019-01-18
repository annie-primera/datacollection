from flask import Flask, current_app
from blinker import Namespace

sample_signal = Namespace()

def summary_signal(datacollection, message):
