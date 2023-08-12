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


def download_video(input_link: str, output_folder: str = None):
    """
    Download Video

    :param input_link: Input Video Link
    :param output_folder: Output folder
    :return:
    """
    if output_folder is None:
        output_folder = default_configs.get("download_path")
    else:
        output_folder = pathlib.Path(output_folder)
    output_folder.mkdir(exist_ok=True, parents=True)

    try:
        obj = YouTube(input_link)
        obj.streams.filter(progressive=True, file_extension="mp4")\
            .order_by("resolution")\
            .desc()\
            .first()\
            .download(output_path=output_folder.as_posix())

        # https://stackoverflow.com/questions/70776558/pytube-exceptions-regexmatcherror-init-could-not-find-match-for-w-w
        print("Download completed successfully")
    except Exception as e:
        print(e.__str__())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", help="Video URL", type=str, dest="input_link")
    parser.add_argument("-d", help="Output Video path", type=str, dest="output_folder")
    args = parser.parse_args()

    download_video(**args.__dict__)
