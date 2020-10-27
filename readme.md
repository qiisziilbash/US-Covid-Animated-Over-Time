[![Watch the video]](https://www.youtube.com/watch?v=dkWlypeWqt8&ab_channel=KnowledgeCrawler)
- Command for making video of the images (10 image per second; 30 fps)
    - ```$ ffmpeg -framerate 10 -pattern_type glob -i '*.png' -c:v libx264 -r 30 -pix_fmt yuv420p out.mp4```
- command for batch image annotation:
    - ```$ mogrify -path out/ -gravity North  -background Khaki   -splice 0x18 -annotate +0+2 '%t' *.png ```
