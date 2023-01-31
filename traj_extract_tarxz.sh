#!/usr/bin/env zsh

function trap_ctrlc() {
   # perform cleanup here

   if [[ -d "$incompletefolder" ]]; then
     rm -rf $incompletefolder
     echo "Ctrl-C...Deleted incomplete folder: $incompletefolder/"
   fi

   # exit shell script with error code 2
   exit 2
}

incompletefolder=""
trap "trap_ctrlc" 2

for a in *.tar.xz
do
    a_dir=${a%.tar.xz}
    if [ ! -d "$a_dir" ]; then
        echo "$a: Extracting to folder $a_dir..."
        incompletefolder=$a_dir
        mkdir -p $a_dir
        tar -xzf $a -C $a_dir
        incompletefolder=""
    else
        # echo "$a: folder already exists. Skipping"
    fi
done
