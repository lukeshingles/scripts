#!/usr/bin/env zsh
set -e
set -o pipefail

#!/usr/bin/env zsh

if [ $# -eq 0 ]; then
  echo 1>&2 "Usage: $0 [file ...]"
  exit 3
fi

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
      if [[ ${file##*\.}  == 'gz' ]]; then
        fileorig=${file%.gz}
        echo decompressing $file
        du -h $file
        gunzip "$file"
      else
        fileorig=$file
      fi

      du -h $fileorig

      filexz=$fileorig.xz

      # ORIGSUM=$(sha1sum < $fileorig)

      if [[ -f "$filexz" ]]; then
        read "confirmoverwrite?$filexz already exists! Overwrite? [y]"
        if [[ "$confirmoverwrite" =~ ^[Yy]$ ]]
        then
          overwriteflag="-f"
        fi
      fi
      xz --best -T0 $overwriteflag -v $fileorig
      du -h $filexz

      # NEWSUM=$(unxz -c $filexz | sha1sum)

      # if xz -t "$filexz"; then
      #   echo $filexz is good according to xz
      #   if [ "${ORIGSUM}" = "${NEWSUM}" ]; then
      #     rm $fileorig
      #     echo checksum matched. deleted $fileorig
      #   else
      #     echo checksum mismatch. not deleting $fileorig
      #   fi
      # fi
    fi
  else
    echo File "$file" does not exist
  fi
done

