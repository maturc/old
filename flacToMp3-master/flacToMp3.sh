#!/bin/bash

#when running the script, the path to the flac folder is needed as an argument

path=$1

echo "Choose one by writing it's number:"
echo "1. V2"
echo "2. V0"
echo "3. 320"
read p

if [ $p -eq 1 ]; then
    folder="MP3 V2"
    param="-V2 -h"
elif [ $p -eq 2 ]; then
    folder="MP3 V0"
    param="-V0 -h"
elif [ $p -eq 3 ]; then
    folder="MP3 320"
    param="-b 320 --cbr -h"
else
    echo "Wrong option, try again."
    exit 127
fi

flac -d "$path"/*.flac

mkdir "$path/$folder"

filename="wav.txt"
ls "$path" | grep '.wav' > "$path/$filename"

while read -r line
do
    name=${line%.*}
    echo "File being converted: $name"
    lame "$path/$name.wav" "$path/$folder/$name.mp3" $param
done < "$path/$filename"

sudo rm "$path/$filename"


