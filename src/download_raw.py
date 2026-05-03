from pathlib import Path
from urllib.request import urlopen as url
import shutil


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_URL = "https://opendata.cern.ch/record/93949/files/00334566_00000001_1.dvntuple.root"
OUTPUT_DIR = BASE_DIR / "data" / "raw"


def download_file():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    filename = DATA_URL.split("/")[-1]

    output_path = OUTPUT_DIR / filename

    if output_path.exists():
        print(f'{output_path} already exists')
        return
    print(f'Downloading from {DATA_URL}')


    with url(DATA_URL) as response:
        if response.status != 200:
            raise Exception(f'Failed to download file: {response.status}')
        with open(output_path, "wb") as file:
            shutil.copyfileobj(response, file)

        print(f'Saving to {output_path}')
        print(f'Download complete')
    return

if __name__ == '__main__':
    download_file()