import os
import asyncio
import aiohttp
from tqdm import tqdm
from zipfile import ZipFile
from utils import (
    repeater
)
from concurrent.futures import (
    ProcessPoolExecutor, 
    as_completed
)

# 파일을 다운로드하고 압축 해제하는 기능을 제공하는 클래스
class DownloadManager:
    def __init__(self,
                 path='temp/downloaded',
                 unzipped_path='temp/unzipped',
                 unzip=True):
        
        self.path = path
        self.unzip = unzip
        self.unzipped_path = unzipped_path

    # URL 목록을 주어진 크기로 나누는 함수
    def chunk(self, urls, chunks=5):
        # return [urls[i:1] for i in range(0, len(urls), chunks)]           # 테스트용 코드
        return [urls[i:i + chunks] for i in range(0, len(urls), chunks)]
    
    # 주어진 zip 파일의 압축 해제
    def unzip_xml(self, fname):
        with ZipFile(fname, 'r') as zf:
            uncompress_size = sum((file.file_size for file in zf.infolist()))
            with tqdm(total=uncompress_size, unit='B', unit_scale=True, desc=f'Unzipping {os.path.basename(fname)}') as pbar:
                for file in zf.infolist():
                    extracted_path = zf.extract(file, self.unzipped_path)

                    with open(extracted_path, 'rb') as f:
                        while True:
                            chunk = f.read(1024)
                            if not chunk:
                                break
                            pbar.update(len(chunk))

    # 압축해제 프로세스 관리 : 멀티프로세싱 ( ProcessPoolExecutor )
    def unzip_xmls(self, batch):
        with ProcessPoolExecutor() as executor:
            futures = {executor.submit(self.unzip_xml, datum): datum for datum in batch}
            for future in as_completed(futures):
                future.result()

    # 비동기 방식으로 파일 다운로드
    @repeater
    async def download(self, session, url, fname):
        if os.path.isfile(fname):
            return
        
        async with session.get(url) as response:
            total_size = int(response.headers.get('content-length', 0))
            pbar = tqdm(total=total_size, unit='iB', unit_scale=True, desc=fname)

            with open(fname, 'wb') as f:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
                    pbar.update(len(chunk))
            pbar.close()

    # 다운로드 프로세스 관리 ( 최신 URL 다운로드 ) : 비동기 방식 ( ClientSession )
    async def download_wrapper(self, url):
        os.makedirs(self.path, exist_ok=True)

        async with aiohttp.ClientSession() as session:
            local_fname = os.path.join(self.path, os.path.basename(url))
            return await self.download(session=session, url=url, fname=local_fname)

    # 다운로드 프로세스 관리 ( 모든 URL 다운로드 ) : 비동기 방식 ( ClientSession )
    async def download_files(self, urls):
        os.makedirs(self.path, exist_ok=True)

        async with aiohttp.ClientSession() as session:
            tasks=[]
            for url in urls:
                local_fname = os.path.join(self.path, os.path.basename(url))
                tasks.append(self.download(session, url, local_fname))

            await asyncio.gather(*tasks)