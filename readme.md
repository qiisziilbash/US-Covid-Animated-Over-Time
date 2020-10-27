
<h1 align="center">Covid Cases in the US over time</h1>
<br>
<p align="center">
    <a href='https://www.youtube.com/watch?v=dkWlypeWqt8&ab_channel=KnowledgeCrawler'>
          <img width="460" height="300" src="https://github.com/qiisziilbash/US-Covid-Animated-Over-Time/blob/master/data/output.gif">
    </a>
    <br>
    <b>Click on the picture to see the full animation</b>
</p>

<br>
<br>
<br>

### Some commands used for making the animation
- Command for making video of the images (10 image per second; 30 fps)
    - ```$ ffmpeg -framerate 10 -pattern_type glob -i '*.png' -c:v libx264 -r 30 -pix_fmt yuv420p out.mp4```
- command for batch image annotation:
    - ```$ mogrify -path out/ -gravity North  -background Khaki   -splice 0x18 -annotate +0+2 '%t' *.png ```
