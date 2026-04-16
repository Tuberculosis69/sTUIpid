#!/bin/bash
javac -cp lib/gson-2.10.1.jar:lib/lanterna-3.1.1.jar *.java
java -cp .:lib/gson-2.10.1.jar:lib/lanterna-3.1.1.jar Main