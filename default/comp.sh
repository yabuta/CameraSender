#!/bin/bash

g++ -o test test.cpp `pkg-config --cflags opencv` `pkg-config --libs opencv`

