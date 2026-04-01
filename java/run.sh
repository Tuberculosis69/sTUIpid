#!/bin/bash
find . -type d -name __pycache__ -exec rm -rf {} +
python3 main.py
javac -cp gson-2.10.1.jar *.java
java -cp .:gson-2.10.1.jar Main