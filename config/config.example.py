# Copy this file to config.py

# Where the series will be put after they've been downloaded and (rerendered)
# Examples
# SERIES_DIR = '/mnt/lvm/series'
# SERIES_DIR = 'E:\\series'
SERIES_DIR = ""

# (Optional) How many threads you want to use when rendering. Defaults to 1
THREADS = 8

# (Optional) How much faster you want to speed up the videos you download. This setting can be overridden for
# each of the channels. Defaults to 1 (i.e., no change in speed)
SPEED_UP_DEFAULT = 1.5

# (Optional) Maximum number of days since the episode was released. If older than this we don't download it.
# Setting the value to 0 disabled it. This value can also be set from the program arguments.
# Defaults to 3.
MAX_DAYS_BACK = 6

# Here are all the channels you want to download
CHANNELS = {
    "Friendly Channel Name": {
        # You can get the channel ID by __FIRST__ going to one of their videos, then pressing on their name.
        # The channel id is then available in your URL
        "channel_id": "UCcJgOeune0II4a_qi9OMkRA",
        
        # (Optional) If you want this series folder to end up in another dir under SERIES_DIR.
        # Equals to <<dir>> in SERIES_DIR/<<dir>>/CHANNEL_NAME/Season 01/TITLE - s01e01.mp4
        "dir": "gaming",  # In this the videos will be under "/mnt/lvm/series/gaming/Friendly Channel Name/Season 01/title - s01e01.mp4
        
        # (Optional) If you want to set another speed than SPEED_UP_DEFAULT
        "speed": 2.0,
        
        # (Optional) Include patterns in regex format
        # If the include pattern is set, only titles that match one of these patterns will be downloaded
        "includes": [
            r"tutorial"  # Example, only download videos that contain the word 'tutorial'
        ],
        
        # (Optional) Exclude patterns in regex format. Can't be used together with 'include'.
        # If the exclude pattern is set, titles that match any of the exclude patterns won't be downloaded
        "excludes": [
            r"wordpress"  # Example, download all videos except those that have the title 'wordpress'
        ],
    },
}
