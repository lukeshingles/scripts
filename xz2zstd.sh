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
    if [[ ${file##*\.}  == 'zst' ]]; then
      echo $file is already zstd
      # if zstd -t "$file"; then
      #   echo $file is good!
      # else
      #   echo $file is bad!
      # fi
    else
      echo " "
      du -h $file
      if [[ ${file##*\.}  == 'xz' ]]; then
        filezstd=${file%.xz}.zst
      else
        filezstd=$file.zst
      fi

      SKIPFILE=false
      if [[ -f "$filezstd" ]]; then
        if [[ ${file##*\.}  == 'xz' ]]; then
          ORIGSUM=$(xz -d -T0 --to-stdout $file | shasum)
          echo "$ORIGSUM ($(basename $file) xzip uncompressed checksum)"
        else
          ORIGSUM=$(shasum < $file)
          echo "$ORIGSUM ($(basename $file) original file checksum)"
        fi
        ZSTDORIGSUM=$(zstd -d -T0 --stdout $filezstd | shasum)
        echo "$ZSTDORIGSUM ($(basename $filezstd) zstd uncompressed checksum)"
        if [ "${ORIGSUM}" = "${ZSTDORIGSUM}" ]; then
          rm $file
          echo "$(basename $filezstd) exists and data checksum matches $(basename $file). Deleted $(basename $file)"
          SKIPFILE=true
        else
          echo "WARNING: checksum mismatch! existing zstdip file contains different data"

          read "confirmoverwrite?$(basename $filezstd) already exists! Overwrite? [y/n]"
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
          # uncompress xzip and compress zstdip

          incompletefile=$filezstd
          xz -d -T0 -k < "$file" | zstd -T0 -f -v -20 > "$filezstd"
          incompletefile=""

          ORIGSUM=$(xz -d -T0 --to-stdout $file | shasum)
          echo "$ORIGSUM ($(basename $file) xzip uncompressed checksum)"

          NEWSUM=$(zstd -d -T0 --stdout $filezstd | shasum)
          echo "$NEWSUM ($(basename $filezstd) zstd uncompressed checksum)"

          if zstd -t "$filezstd"; then
            if [ "${ORIGSUM}" = "${NEWSUM}" ]; then
              rm $file
              echo "$(basename $filezstd) is good and checksum matched. Deleted $(basename $file)"
            else
              rm $filezstd
              echo "ERROR: checksum mismatch! Did not delete $(basename $file)"
              read "Press enter to continue"
            fi
          else
            rm $filezstd
            echo "ERROR: $(basename $filezstd) is bad according to zstd!"
            read "Press enter to continue"
          fi
        else
          zstd -T0 -f -v -20 --rm $file
        fi
      fi
    fi
  else
    echo "File $file does not exist"
  fi
done

