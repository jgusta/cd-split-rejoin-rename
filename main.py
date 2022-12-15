import time
from pydub import AudioSegment
from pather import Pather
from pather import clean_filename
from pydub.silence import split_on_silence
import argparse
import os
from termcolor import cprint

if __name__ == '__main__':
    currentDir = os.getcwd()
    timestr = time.strftime("%Y%m%d-%H%M%S")
    parser = argparse.ArgumentParser(description="Combine sound files into one file.")
    parser.add_argument('input',
                        type=Pather.arg_type,
                        help="Directory where to pull files from. Defaults to current directory.",
                        default=currentDir)
    parser.add_argument(
        "--map",
        required=False,
        help="A pipe-separated list of track number, artist and title",
        default=None)

    parser.add_argument(
        "--base",
        required=False,
        help="Basename for the output, if no --map",
        default=None)

    args = parser.parse_args()

    if args.base is None:
        base = clean_filename(f"{args.input}-sliced")
    else:
        base = clean_filename(f"{args.base}")

    output_dir_name = os.path.join(currentDir, clean_filename(base))

    if os.path.exists(output_dir_name):
        cprint(output_dir_name + ' exists, will not overwrite.', "red")
        exit()

    p = Pather(args.input)
    waves = p.get_files_full_paths('wav')
    count = len(waves)

    map_spec = None

    if args.map:
        try:
            with open(args.map, "r") as mapfile:
                map_spec = mapfile.read().splitlines()
        except:
            cprint('bad map', "red")
            exit()

    os.mkdir(output_dir_name)

    list_idx = 0
    list_max = None
    if map_spec:
        list_max = len(map_spec)

    for i in range(0, count):
        cur = waves[i]

        with open(cur, "rb") as sound:
            cprint(f"\n{cur}", "blue")
            segment1 = AudioSegment.from_file(sound)
            audio_chunks = split_on_silence(segment1, min_silence_len=600, silence_thresh=-80, seek_step=10,
                                            keep_silence=False)

            mylength = len(audio_chunks)
            if mylength > 3:
                cprint("Found " + str(mylength) + " Sounds", "magenta")
            else:
                cprint("Found " + str(mylength) + " Sounds", "blue")

            for j, chunk in enumerate(audio_chunks):
                if map_spec:

                    if list_idx >= list_max:
                        cprint(f"Ran out of names in the map! > {list_max}", "red")
                        exit()

                    map_chunks = map_spec[list_idx].split('|')
                    # cprint(map_spec[list_idx], "blue")
                    numb = map_chunks[0].zfill(3)
                    piece_name = f'{numb} - {map_chunks[1]} - {map_chunks[2]}.wav'
                    output_file = os.path.join(output_dir_name, clean_filename(piece_name))
                    list_idx += 1
                else:
                    numb = str(j).zfill(3)
                    output_file = os.path.join(output_dir_name, clean_filename(f'{base}-chunk-{numb}.wav'))

                if os.path.exists(output_file):
                    cprint(output_file + ' exists, will not overwrite.', "red")
                    exit()

                cprint(f"writing {output_file}", "green")

                with open(output_file, "wb") as outfile:
                    chunk.export(outfile, format="wav")

            if map_spec:
                cprint(f"{list_max - list_idx} names left.", "yellow")