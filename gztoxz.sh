#!/usr/bin/env zsh
set -e
set -o pipefail

#!/usr/bin/env zsh

if [ $# -eq 0 ]; then
  echo 1>&2 "Usage: $0 [file ...]"
  exit 3
fi

for filegz in "$@"
do
  if [[ -f "$filegz" ]]; then
    if [[ ${filegz##*\.}  == 'gz' ]]; then
      filexz=${filegz%.gz}.xz
      echo Converting $filegz to $filexz

      ORIGSUM=$(gzip -dc $filegz | tee >(xz --best -v > $filexz) | sha1sum)
      NEWSUM=$(unxz -c $filexz | sha1sum)
      if [ "${ORIGSUM}" = "${NEWSUM}" ]; then rm -v $filegz; fi
    else
      echo File "$filegz" does not end in .gz
    fi
  else
    echo File "$filegz" does not exist
  fi
done

