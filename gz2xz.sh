#!/usr/bin/env zsh
set -e
set -o pipefail

#!/usr/bin/env zsh

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
    if [[ ${file##*\.}  == 'xz' ]]; then
      echo $file is already xzipped
      # if xz -t "$file"; then
      #   echo $file is good!
      # else
      #   echo $file is bad!
      # fi
    else
      echo " "
      du -h $file
      if [[ ${file##*\.}  == 'gz' ]]; then
        filexz=${file%.gz}.xz
      else
        filexz=$file.xz
      fi

      SKIPFILE=false
      if [[ -f "$filexz" ]]; then
        if [[ ${file##*\.}  == 'gz' ]]; then
          ORIGSUM=$(gunzip -c $file | shasum)
          echo "$ORIGSUM ($(basename $file) gzip uncompressed checksum)"
        else
          ORIGSUM=$(shasum < $file)
          echo "$ORIGSUM ($(basename $file) original file checksum)"
        fi
        XZORIGSUM=$(unxz -c $filexz | shasum)
        echo "$XZORIGSUM ($(basename $filexz) xz uncompressed checksum)"
        if [ "${ORIGSUM}" = "${XZORIGSUM}" ]; then
          rm $file
          echo "$(basename $filexz) exists and data checksum matches $(basename $file). Deleted $(basename $file)"
          SKIPFILE=true
        else
          echo "WARNING: checksum mismatch! existing xzip file contains different data"

          read "confirmoverwrite?$(basename $filexz) already exists! Overwrite? [y/n]"
          if [[ "$confirmoverwrite" =~ ^[Yy]$ ]]
          then
            SKIPFILE=false
          else
            SKIPFILE=true
          fi
        fi
      fi

      if [ "$SKIPFILE" = false ]; then
        if [[ ${file##*\.}  == 'gz' ]]; then
          # uncompress gzip and compress xzip

          incompletefile=$filexz
          gunzip < "$file" | xz -T0 -f -v --best > "$filexz"
          incompletefile=""

          ORIGSUM=$(gunzip -c $file | shasum)
          echo "$ORIGSUM ($(basename $file) gzip uncompressed checksum)"

          NEWSUM=$(unxz -c $filexz | shasum)
          echo "$NEWSUM ($(basename $filexz) uncompressed checksum)"

          if xz -t "$filexz"; then
            if [ "${ORIGSUM}" = "${NEWSUM}" ]; then
              rm $file
              echo "$(basename $filexz) is good and checksum matched. Deleted $(basename $file)"
            else
              rm $filexz
              echo "ERROR: checksum mismatch! Did not delete $(basename $file)"
              read "Press enter to continue"
            fi
          else
            rm $filexz
            echo "ERROR: $(basename $filexz) is bad according to xz!"
            read "Press enter to continue"
          fi
        else
          xz -T0 -f -v --best $file
        fi
      fi
    fi
  else
    echo "File $file does not exist"
  fi
done

