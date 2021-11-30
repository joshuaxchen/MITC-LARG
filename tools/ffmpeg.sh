# Rename all *.txt to *.text
for f in *.mp4; do 
    #mv -- "$f" "${f%.txt}.text"
	ffmpeg -i "$f" -pix_fmt yuv420p "${f%.mp4}.mov"
done

