#!/bin/bash


frame=0
index=0
step=76
time_step=100  # ps per frame


### NOTE -- THIS WILL CONTINUE INDEFININETELY, NEED TO MANUALLY BREAK LOOP
while true; do
    time_ps=$((frame * time_step))

    gmx trjconv -s template.pdb -f pbc_no_jump_skip_100_center.xtc -dump $time_ps -sep -o pair${index}.pdb <<< "0"

    # Break if trjconv fails (e.g., due to reaching the end of the trajectory)
    if [ $? -ne 0 ]; then
        echo "Reached end of trajectory or error occurred."
        break
    fi

    frame=$((frame + step))
    index=$((index + 1))
done


### move them all into folders
files=(pair*.pdb)

# Loop through the files with a counter
for i in "${!files[@]}"; do
    dir="rep_$i"
    mkdir -p "$dir"                     # Create the directory
    mv "${files[$i]}" "$dir/"          # Move the file into the directory
done

