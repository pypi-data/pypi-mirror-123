# This is a typing effect
import time
import sys


def typingprint(text):
    """Typingprint types out stuff"""
    for character in text:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)