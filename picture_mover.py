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

def get_files_in_db(db_file):
    dbconn = sqlite3.connect(db_file)
    dbcursor = dbconn.cursor()
    photo_files = get_filenames_from_table(dbcursor, "PhotoTable")
    video_files = get_filenames_from_table(dbcursor, "VideoTable")
    dbconn.close()
    return video_files.union(photo_files)

def get_filenames_from_table(cursor, table_name):
    return set(map(operator.itemgetter(0), cursor.execute("SELECT filename FROM " + table_name).fetchall()))

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

home = os.environ["HOME"]
db_file = home + "/.local/share/shotwell/data/photo.db"
file_directory = home + "/Pictures/Shotwell"
archive_directory = home + "/Pictures/Shotwell_archive"

files_on_disc = get_files_with_suffixes_any_case(["jpg", "jpeg", "mov", "mp4"])
files_in_db = get_files_in_db(db_file)
files_to_archive = files_on_disc - files_in_db
archive_files(files_to_archive, file_directory, archive_directory)
print("{} files archived".format(len(files_to_archive)))

