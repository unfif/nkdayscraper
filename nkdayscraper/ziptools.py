from zipfile import ZipFile, ZIP_DEFLATED
from concurrent.futures import ThreadPoolExecutor
import logging

class ZipTools:
    def zipWithInfo(self, zipPath, filePath):
        logging.info(f'making {zipPath=}')
        with ZipFile(zipPath, 'w', ZIP_DEFLATED) as zip:
            zip.write(filePath, filePath.name)
        logging.info(f'zipped {filePath=}')

    def zipEachFilesInDir(self, dirPath):
        with ThreadPoolExecutor(max_workers=8) as executor:
            for jsonPath in dirPath.iterdir():
                if jsonPath.suffix == '.json':
                    zipPath = dirPath / f'{jsonPath.stem}.zip'
                    executor.submit(self.zipWithInfo, zipPath, jsonPath)

if __name__ == '__main__':
    from sys import argv
    logging.basicConfig(
        level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
    )
    if len(argv) > 1:
        from pathlib import Path
        zipDir = Path(argv[1])
        zipTools = ZipTools()
        zipTools.zipEachFilesInDir(zipDir)
    else:
        logging.info('No file was Zipped.')
        