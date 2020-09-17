#!/usr/bin/env python3
"""
Amazon Order Alert
"""

__author__ = "Chris Loidolt"
__version__ = "0.1.0"
__license__ = "GNU 3.0"

from shipstation import getOrders

def main():
    """ Main entry point of the app """
    getOrders()

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()