#! /bin/bash

# find all python files
x=$(find . -name "*.py");
echo $x;
y=', ' read -r -a array <<< $x
echo "$y";

# create mpy files
for idx in "${!array[@]}"
do
echo "$idx ${array[idx]}"
lab=$( echo "${array[idx]}" | cut -d '.' -f 2 | cut -d '/' -f 2);
mpy-cross -o "./$lab.mpy" "./$lab.py";
echo "$lab";
done

# copy mpy files to device.
