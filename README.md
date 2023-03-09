# cd-split-rejoin-rename

A one-off python script to assist with organizing content from audio sample CDs (compact disks).

This script helps to organize the contents of audio sample CDs by splitting, rejoining, and renaming individual WAV files based on the track listing of the CD. Though not designed to be universally useful outside my one use case, it might save someone some time with a few modifications.

TL;DR: Multi-CD sample collections + track listing ==> Individual named WAV files.

Audio sample collections were often distributed on uncompressed Audio CDs in the 90s. These CDs were limited by the linear nature of their format and the maximum number of tracks that could be used on any one disk, making it difficult to organize the contents. This script provides a solution by splitting and renaming the individual WAV files based on the track listing.

To use the script, input each track of a multi-CD collection in WAV format, ordered alphabetically, and a list of all the individual sample names/descriptions as a txt file, one sound per line. The script concatenates all of the WAV files together into one file, then splits them using a length of silence as a delimiter. It then uses the name list to name each file.

If working with ISO files, the `bchunk` command-line tool available in your local package manager can be used to convert bin/cue files to ISO and split them into WAV files.

Note: Fine-tuning may be required for optimal results.
