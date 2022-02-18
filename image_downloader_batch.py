import os
from tqdm import tqdm
import urllib.request
import datetime
import pandas as pd
import numpy as np
import zipfile

class downloader:
    '''이미지 URL DataFrame을 입력받아 배치 단위로 이미지 다운로드
    '''
    def __init__(self, urls, batch_size: int):
        self.data = urls
        self.file_size = len(self.data)
        self.batch_size = batch_siz
        
    def batch_generator(self):
        '''배치 생성 함수
        '''
        for batch_number, batch_df in self.data.groupby(np.arange(self.file_size) // self.batch_size):
            yield batch_number, batch_df
    
    def make_file(self, target_directory):
        '''사진 저장 폴더 생성 함수
        '''
        os.mkdir(target_directory)
        
    def comp_file(self, target_directory):
        '''사진이 저장된 폴더 압축 함수
        '''
        
        zip_file = zipfile.ZipFile(target_directory + ".zip", 'w', compression=zipfile.ZIP_DEFLATED)
        for (path, dir, files) in os.walk(target_directory): 
            for file in files: 
                if file.endswith('.jpg'): 
                    zip_file.write(os.path.join(path, file), 
                                   os.path.relpath(os.path.join(path,file), 
                                                   "your/directory"), # 시작 파일 지정 - zipfile은 압축시 경로의 모든 상위폴더들을 포함해서 압축시킨다.
                                    compress_type=zipfile.ZIP_DEFLATED)
        zip_file.close()

    def delete_file(self, target_directory):
        '''압축 파일 생성을 위한 폴더 제거 함수
        '''
        if os.path.exists(target_directory):
            shutil.rmtree(target_directory)
        else:
            pass
        
    def print_info(self, batch_number, target_directory):
        '''다운로드 정보 출력 함수
        '''
        print(batch_number, " --done-- ")
        print("[DOWNLOAD INFO]")
        print(f"{datetime.datetime.now()}: image_file_{batch_number}_batch.zip")
        print("---------------")
        
    def download(self):
        print("download thumbnail image..")
        print("[DOWNLOAD CONFIG]")
        print(f"Batch Size: {self.batch_size}")
        print(f"Total File Size: {self.file_size}")
        print("----------------------------------")
        
        for batch_number, batch_df in self.batch_generator():
            target_directory = f"your/directory/image_file_{batch_number}_batch"
            self.make_file(target_directory)
            
            url_ = batch_df['thumbnail_url'].map(lambda x: x[0])
            user_id = batch_df['id']
            for i, url in zip(user_id, url_):
                filename = target_directory + f"/test_data_{i}.jpg"
                urllib.request.urlretrieve(url, filename)
            
            self.comp_file(target_directory)
            self.delete_file(target_directory)
            
            self.print_info(batch_number, target_directory)
    
    
down = downloader(test_data, 30)
down.download()
