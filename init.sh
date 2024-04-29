mkdir $1
curl --cookie cookie_jar.txt https://adventofcode.com/2023/day/{$1}/input -o $1/input.txt
