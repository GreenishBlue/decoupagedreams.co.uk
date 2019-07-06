for f in *.jpg; do
  convert "$f" -filter Gaussian -blur 0x64 ./"${f}.blur.jpg"
done
