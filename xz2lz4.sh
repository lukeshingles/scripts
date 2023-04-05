#!/usr/bin/env zsh
set -e
set -o pipefail

if [ $# -eq 0 ]; then
  echo 1>&2 "Usage: $0 [file ...]"
  exit 3
fi


function trap_ctrlc() {
   # perform cleanup here

   if [[ -f "$incompletefile" ]]; then
     rm $incompletefile
     echo "Ctrl-C caught...deleted incomplete file: $incompletefile"
   fi

   # exit shell script with error code 2
   exit 2
}

trap "trap_ctrlc" 2

for file in "$@"
do
  if [[ -f "$file" ]]; then
    if [[ ${file##*\.}  == 'lz4' ]]; then
      echo $file is already lz4
      # if lz4 -t "$file"; then
      #   echo $file is good!
      # else
      #   echo $file is bad!
      # fi
    else
      echo " "
      du -h $file
      if [[ ${file##*\.}  == 'xz' ]]; then
        filelz4=${file%.xz}.lz4
      else
        filelz4=$file.lz4
      fi

      SKIPFILE=false
      if [[ -f "$filelz4" ]]; then
        if [[ ${file##*\.}  == 'xz' ]]; then
          ORIGSUM=$(xz -d --to-stdout $file | shasum)
          echo "$ORIGSUM ($(basename $file) xzip uncompressed checksum)"
        else
          ORIGSUM=$(shasum < $file)
          echo "$ORIGSUM ($(basename $file) original file checksum)"
        fi
        lz4ORIGSUM=$(lz4 -d --to-stdout $filelz4 | shasum)
        echo "$lz4ORIGSUM ($(basename $filelz4) lz4 uncompressed checksum)"
        if [ "${ORIGSUM}" = "${lz4ORIGSUM}" ]; then
          # rm $file
          echo "$(basename $filelz4) exists and data checksum matches $(basename $file). Deleted $(basename $file)"
          SKIPFILE=true
        else
          echo "WARNING: checksum mismatch! existing lz4ip file contains different data"

          read "confirmoverwrite?$(basename $filelz4) already exists! Overwrite? [y/n]"
          if [[ "$confirmoverwrite" =~ ^[Yy]$ ]]
          then
            SKIPFILE=false
          else
            SKIPFILE=true
          fi
        fi
      fi

      if [ "$SKIPFILE" = false ]; then
        if [[ ${file##*\.}  == 'xz' ]]; then
          # uncompress xzip and compress lz4ip

          incompletefile=$filelz4
          xz -d -k < "$file" | lz4 -f -v --best > "$filelz4"
          incompletefile=""

          ORIGSUM=$(xz -d --to-stdout $file | shasum)
          echo "$ORIGSUM ($(basename $file) xzip uncompressed checksum)"

          NEWSUM=$(lz4 -d --to-stdout $filelz4 | shasum)
          echo "$NEWSUM ($(basename $filelz4) uncompressed checksum)"

          if lz4 -t "$filelz4"; then
            if [ "${ORIGSUM}" = "${NEWSUM}" ]; then
              # rm $file
              echo "$(basename $filelz4) is good and checksum matched. Deleted $(basename $file)"
            else
              rm $filelz4
              echo "ERROR: checksum mismatch! Did not delete $(basename $file)"
              read "Press enter to continue"
            fi
          else
            rm $filelz4
            echo "ERROR: $(basename $filelz4) is bad according to lz4!"
            read "Press enter to continue"
          fi
        else
          lz4 -T0 -f -v --best $file
        fi
      fi
    fi
  else
    echo "File $file does not exist"
  fi
done

