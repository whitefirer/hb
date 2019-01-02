#!/bin/bash

find . -type d -name "__pycache__" | xargs rm -rf
