# media_editing

# setup

```Bash
pip install media_editing
```

# Markdown_to_HTML.py

This script recursively converts Markdown files at a specified directory to HTML files, with options to include numbered sections, table of contents, CSS and to output commands only, not execute.

Example usage with CSS specified is as follows:

```Bash
cd my_writing_files_in_Markdown

CSS="https://raw.githack.com/wdbm/style/master/SS/bluescale.css"
Markdown_to_HTML.py --CSS="${CSS}"
```

# images_to_video.py

This script converts a list of image files to a video with the options of specifying the image extension, a soundtrack file, an output filename and a framerate.

# text_to_QR_code.py

This script converts specified text to a QR code of specified scale and filepath and optionally displays the resulting QR code image using the default image viewer.

# vidgif.py

This script converts a video to an animated GIF, with the option to output commands only, not execute.

# OCR of region of display

```Bash
sudo apt install imagemagick scrot tesseract-ocr
```

```Bash
tmp="$(mktemp)"
scrot -s "${tmp}".png -q 100 
mogrify -modulate 100,0 -resize 400% "${tmp}".png 
tesseract "${tmp}".png "${tmp}" &> /dev/null
cat "${tmp}".txt
```

---

# High Dynamic Resolution (HDR)

## Luminance HDR

### setup

```Bash
sudo apt update
sudo apt install luminance-hdr
```

### settings used to combine a darker and a lighter image 2019-02-24

- tonemap
    - operator: Reinhard '05
    - brightness: -10
    - chromatic adaptation: 0
    - light adaptation: 1
- process
    - pre-gamma: 0.86

---

# recording internal audio: audio-recorder

## setup

```Bash
sudo dpkg -i audio-recorder_1.7-5~xenial_amd64.deb
```

## usage

```Bash
audio-recorder
```

- Under "Audio settings.", select the source as something like "Clear Chat Comfort USB Headset (Audio output)".
- Select "Start recording".

![](https://raw.githubusercontent.com/wdbm/media_editing/master/media/Audio_Recorder.png)

---

# FFmpeg

## trim video using start and stop times without reencoding

Note the ordering of the command line arguments and options.

```Bash
filepath_1="Star.Wars.1977.Despecialized.720p.x264.AC3.5.1.mkv"
filepath_2="out.mkv"
start="01:40:33"
stop="01:54:48"

time ffmpeg -y -i "${filepath_1}" -ss "${start}" -to "${stop}" -c copy "${filepath_2}"
```

## remove audio from video

The `-an` flag is used.

```Bash
ffmpeg -i in.mkv -c copy -an out.mkv
```

---

# ImageMagick

## change quality of directory of JPEG images

```Bash
mogrify -quality 95 *.jpg
```

## strip/remove an image of all profiles and comments using ImageMagick

```Bash
convert -strip image_1.png image_2.png
```

```Bash
mogrify -strip *.jpg
```

## create an image of specified width, height and color using ImageMagick

Width is specified before height.

```Bash
convert -size 100x100 xc:#000000 out.png
```

```Bash
convert -size 100x100 xc:rgba\(255,0,0,0.4\) out.png
```

```Bash
width_pixels="3495"
height_pixels="2160"
color="#eeeeee"
filepath="out.png"
convert -size "${width_pixels}"x"${height_pixels}" xc:"${color}" "${filepath}"
```

```Bash
width_pixels="3107"
height_pixels="1920"
color="#eeeeee"
filepath="background.png"
convert -size "${width_pixels}"x"${height_pixels}" xc:"${color}" "${filepath}"
```

## overlay one foreground image on the center of a background image using ImageMagick

```Bash
convert background.png -coalesce -gravity center -draw 'image over 0,0,0,0 "foreground.png"' out.png
```

```Bash
filepath_foreground="foreground.png"
filepath_background="background.png"
filepath_output="out.png"

# not working, under development:
# time convert "${filepath_background}" -coalesce -gravity center -draw 'image over 0,0,0,0 \"${filepath_foreground}\"' "${filepath_output}"
```

The option `-layers flatten` may be worth considering.

## reduce quality of images at working directory in batch, making new images at new directory

```Bash
mkdir new
mogrify -path new -quality 80 -format jpg *.jpg
```

---

# Inkscape

## set up palettes for Inkscape

```Bash
/usr/share/inkscape/palettes
```

## convert bitmap to vector using Inkscape

- <https://www.youtube.com/watch?v=SjCFRI3knhE>

---

# Calibre

## setup 2019-01-24T0350Z

```Bash
sudo -v && wget -nv -O- https://download.calibre-ebook.com/linux-installer.sh | sudo sh /dev/stdin
```

# view ebook

```Bash
ebook-viewer book.epub
```

# convert EPUB to MOBI using ebook-convert

```Bash
ebook-convert book.epub book.mobi
```

# convert LaTeX to HTML to EPUB

```Bash
mk4ht htlatex book.tex 'xhtml,charset=utf-8,pmathml'
ebook-convert book.html book.epub
```

# convert Markdown to EPUB

```Bash
ebook-convert book.md book.epub
```

---

# music

## some music software and tools

- Audacity
- Hydrogen
- [MidiEditor](https://github.com/markusschwenk/midieditor)
- [MusE](https://muse-sequencer.github.io)
- MuseScore
- [Online Sequencer](https://onlinesequencer.net)

---
