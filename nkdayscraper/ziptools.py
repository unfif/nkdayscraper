from zipfile import ZipFile, ZIP_DEFLATED
from concurrent.futures import ThreadPoolExecutor
import logging

class Ziptools:
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