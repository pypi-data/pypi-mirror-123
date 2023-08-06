# VidEdit

*Command line interface to edit video files based on ffpmeg*

## Usage

### Crop a video

Say you have a video file (`my-record.mkv`) that last 3 minutes, composed of 5 segments (A, B, C, D, E) defined as below...
- A (00:00:00 - 00:00:15)
- B (00:00:15 - 00:00:30)
- C (00:00:30 - 00:01:00)
- D (00:01:00 - 00:02:00)
- E (00:02:00 - 00:03:00)

...and you want to create a new video (`new-video.mkv`) with only segments A, C and E.

You can use the `cut` command like the following :

```bash
videdit cut my-record.mkv -o new-video.mkv  0-15  30-1:0  2:0-3:0
```

**Note**: As you can see, there is no need to specify the time in full format. But you are free to use this longer format :

```bash
videdit cut my-record.mkv -o new-video.mkv  00:00:00-00:00:15  00:00:30-00:01:00  00:02:00-00:03:00
```
