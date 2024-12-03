import functools
import glob
import operator
import os
import sqlite3

def get_files_with_suffixes_any_case(suffixes):
    suffixes_lower = list(map(lambda s: s.lower(), suffixes))
    suffixes_upper = list(map(lambda s: s.upper(), suffixes))
    suffixes_both_cases = suffixes_lower + suffixes_upper
    return get_files_with_suffixes(suffixes_both_cases)

def get_files_with_suffixes(suffixes):
    files = map(lambda suffix: set(glob.glob(file_directory + "/**/*" + suffix, recursive=True)), suffixes)
    return functools.reduce(lambda s1, s2: s2.union(s1), files)

def get_filenames_from_table(cursor, table_name):
    return set(map(operator.itemgetter(0), dbcursor.execute("SELECT filename FROM " + table_name).fetchall()))

def ensure_directory(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def archive_files(files, file_directory, archive):
    for src in files:
        target = src.replace(file_directory, archive)
        target_parts = target.split('/')
        target_dir = '/'.join(target_parts[:-1])
        ensure_directory(target_dir)
        os.rename(src, target)

# Required paths
home = os.environ["HOME"]
db_file = home + "/.local/share/shotwell/data/photo.db"
file_directory = home + "/Pictures/Shotwell"
archive_directory = home + "/Pictures/Shotwell_archive"

# Files on disc
photo_files = get_files_with_suffixes_any_case(["jpg", "jpeg"])
video_files = get_files_with_suffixes_any_case(["mov", "mp4"])

# Files in the database
dbconn = sqlite3.connect(db_file)
dbcursor = dbconn.cursor()
photos_in_db = get_filenames_from_table(dbcursor, "PhotoTable")
videos_in_db = get_filenames_from_table(dbcursor, "VideoTable")
dbconn.close()

# Files to archive
video_files_to_archive = video_files - videos_in_db
photo_files_to_archive = photo_files - photos_in_db
files_to_archive = photo_files_to_archive.union(video_files_to_archive)

ensure_directory(archive_directory)
archive_files(files_to_archive, file_directory, archive_directory)

