# Picture mover

A script for moving jpeg and video files that are located in a specified directory, but not present in the Shotwell database, to an archive directory.

You are free to use the script on your own risk. I recommend taking a backup before!

At the time of writing, pictures and movies (or, more specifically, files with the suffixes 'jpg', 'jpeg', 'mov' or 'mp4', or their capitalized equivalent) are moved from `$HOME/Pictures/Shotwell` to `$HOME/Pictures/Shotwell_archive`, if they cannot be found in of the tables `PhotoTable` or `VideoTable` in the Shotwell database. The directory structure under the source directory is kept.

If you want copy between other directories than the ones stated above, you may change the variables `file_directory` and `archive_directory` inside the script to the source and the target directory paths respectively.

The script is tested on Ubuntu 24.04.

