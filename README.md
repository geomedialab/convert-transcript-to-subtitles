# convert-transcript-to-subtitles

This small Python script Converts a text file containing timestamps of any format to a subtitle file.

The script will prompt you to input a timestamp format with the following question:

> Enter the timestamp format contained in the input text as well as any relevant delimiters (:,;,.) or parentheses ([],(),{}), and use the following characters: HH (for hours), MM (minutes), SS (seconds), 00.. (milliseconds). For example, if your timestamps look like *[01:51:12]*, then enter *[HH:MM:SS]*, other formats could include *MM:SS*, *(H:MM:SS.##)*, *H:MM:SS.###*, etc.), according to https://momentjs.com/docs/#/displaying/format/

The script will then parse your transcript file and output a subtitle file, using the pattern you gave it to detect timestamps in your transcript file and convert them appropriately to subtitle timestamps.

For example:
If you have the following input text:
```
45:11 The champions came through the gates and ran upstairs.

45:30 They yelled with joy

45:35 [...]
```
You would input *MM:SS* in order to produce a subtitle file as follows:

```
00:45:11.000 --> 00:45:30.000
The champions came through the gates and ran upstairs. 

00:45:30.000 --> 00:45:35.000
They yelled with joy
```


