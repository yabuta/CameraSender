#!/bin/bash

g++ -o test2 test2.cpp `pkg-config --cflags opencv` `pkg-config --libs opencv`
