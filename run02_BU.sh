#!/bin/bash

(
    source ./NPenv/bin/activate
    cd bottomUp || exit
    python BUComplete.py
)