import pathlib
import argparse

from pytube import YouTube


default_configs = {
    "download_path": pathlib.Path(pathlib.Path().resolve()).joinpath("downloads")
}


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

    obj = YouTube(input_link)
    obj = obj.streams.get_highest_resolution()

    try:
        obj.download(output_path=output_folder.as_posix())
        print("Download completed successfully")
    except Exception as e:
        print(e.__str__())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", help="Video URL", type=str, dest="input_link")
    parser.add_argument("-d", help="Output Video path", type=str, dest="output_folder")
    args = parser.parse_args()

    download_video(**args.__dict__)
