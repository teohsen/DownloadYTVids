import pathlib
import argparse

# from database.dbtool import create_connection

from pytube import YouTube


default_configs = {
    "download_path": pathlib.Path(pathlib.Path().resolve()).joinpath("downloads"),
    "database": r"./database/pythonsqlite.db"
}


def verify_url(input_link):
    # TODO: Check if http is valid YOUTUBE VIDEO
    pass


def best_progressive(url, output_folder):
    obj = YouTube(url)

    # All in 1
    obj.streams.filter(progressive=True, file_extension="mp4") \
        .order_by("resolution") \
        .desc() \
        .first() \
        .download(output_path=output_folder.as_posix())


def best_adaptive(url, output_folder):
    obj = YouTube(url)

    print("Downloading Video")
    # Download Video
    print(obj.streams.filter(adaptive=True, file_extension="mp4").order_by("resolution").desc().first())
    obj.streams.filter(adaptive=True, file_extension="mp4") \
        .order_by("resolution") \
        .desc() \
        .first() \
        .download(output_path=output_folder.as_posix(), filename_prefix="video-")

    print("Downloading Audio")
    # Download Audio
    print(obj.streams.filter(only_audio=True, file_extension="mp4").order_by("abr").desc().first())

    obj.streams.filter(only_audio=True, file_extension="mp4").order_by("abr").desc().first() \
        .download(output_path=output_folder.as_posix(), filename_prefix="audio-")


    # use VLC or ffmpeg to combine


def download_video(input_link: str, output_folder: str = None, progressive=True):
    """
    Download Video

     # https://stackoverflow.com/questions/70776558/pytube-exceptions-regexmatcherror-init-could-not-find-match-for-w-w

    :param input_link: Input Video Link
    :param output_folder: Output folder
    :param progressive:
    :return:
    """
    if output_folder is None:
        output_folder = default_configs.get("download_path")
    else:
        output_folder = pathlib.Path(output_folder)
    output_folder.mkdir(exist_ok=True, parents=True)

    try:
        if progressive:
            best_progressive(input_link, output_folder)
        else:
            best_adaptive(input_link, output_folder)

        print("Download completed successfully")
    except Exception as e:
        print(e.__str__())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", help="Video URL", type=str, dest="input_link")
    parser.add_argument("-d", help="Output Video path", type=str, dest="output_folder")

    feature_parser = parser.add_mutually_exclusive_group(required=False)
    feature_parser.add_argument("-p", action='store_true', dest="progressive")
    feature_parser.add_argument("-a", action='store_false', dest="progressive")
    args = parser.parse_args()
    parser.set_defaults(progressive=True)

    print(args)
    download_video(**args.__dict__)
