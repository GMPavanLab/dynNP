#!/bin/bash

(
    source ./NPenv/bin/activate
    cd topDown || exit
    #se non ci sono i dile di reference dai reference maker
    python TDcomplete.py
)