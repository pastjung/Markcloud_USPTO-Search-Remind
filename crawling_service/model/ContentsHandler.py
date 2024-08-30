import os
import asyncio
import requests

from model.DownloadManager import DownloadManager
from model.DatabaseManager import DatabaseManager
from utils import (
    logger,
    ProxyRequest,
)    

URL = os.getenv('URL')

# 다운로드 관리와 파일 처리를 담당하는 클래스
class ContentsHandler:
    # 객체 초기화 및 데이터 수집 시작
    def __init__(self, injection):                  # 데이터 파싱을 담당하는 PathTreeParser 인스턴스를 매개변수로 받음
        self.base_url = URL                         # 기본 URL
        self.download_manager = DownloadManager()   # DownloadManaber.py 의 DownloadManager 인스턴스 생성

        try:
            response = ProxyRequest.get(self.base_url)
            item_links = injection.parse(response)  # 추출한 링크들 저장
            self.urls = sorted([f"{self.base_url}{link}" for link in item_links if link.split('.')[-1] == 'zip'])   # 추출한 링크들 중에서 확장자가 zip인 링크만 저장 및 정렬

        except requests.exceptions.Timeout:
            logger.error("\nCould not connect to the USPTO mainpage!")


    # 모든 데이터 다운로드 및 처리
    def get_all(self, mode=None):
        chunks = self.download_manager.chunk(self.urls)          # 저장된 링크들을 지정된 크기의 청크로 나눔
        for chunk in chunks:
            job = self.download_manager.download_files(chunk)    
            asyncio.run(job)                            # 각 청크에 대해 비동기적으로 파일 다운로드

        # self.download_manager.path 디렉토리에 존재하는 모든 파일의 전체 경로를 포함하는 리스트 생성
        self.downloaded = [os.path.join(self.download_manager.path, file) for file in os.listdir(self.download_manager.path)]
        logger.info('\nDownload Completed')
        return self

    # 주어진 URL 리스트(self.urls)에서 가장 최근의 URL을 선택하고, 해당 URL을 다운로드하여 처리
    def get_last(self, mode=None):
        latest = self.urls[-1]                                                                  # 가장 최근 URL 선택
        job = self.download_manager.download_wrapper(latest)                                             # 선택된 URL 다운로드 작업 정의
        asyncio.run(job)                                                                        # 비동기 방식으로 정의한 작업 수행

        filepath = os.path.join(self.download_manager.path, os.path.basename(latest))                    # 다운로드 된 파일의 경로 저장
        if os.path.isfile(filepath):                                                            # os.path.isfile(filepath) : 다운로드 된 파일이 실제로 존재하는지 확인
            self.downloaded = [os.path.join(self.download_manager.path, os.path.basename(latest))]       
        else:
            logger.error(f'No such file as {latest}!')

        return self
        
    # 다운로드된 파일 압축 해제
    def decompress(self, mode=None):
        chunks = self.download_manager.chunk(self.downloaded)    # 저장된 링크들을 지정된 크기의 청크로 나눔
        for chunk in chunks:
            self.download_manager.unzip_xmls(chunk)              # 다운로드된 파일 압축 해제
            
        return self
    
    # 다운로드 및 압축 해제 후 임시 파일 제거 : zip 파일 제거
    def clean_up(self, mode=None):
        for file in self.downloaded:
            os.remove(file)
        print("ZIP: Cleanup completed.")