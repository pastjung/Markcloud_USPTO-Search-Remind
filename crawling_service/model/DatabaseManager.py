import os
from tqdm import tqdm

import xmltodict
from pymongo import UpdateOne

from core.database import collection

class DatabaseManager:
    def __init__(self,
                 path='temp/unzipped',
                 ):
        self.path = path

    def input_files(self):
        xml_files = [os.path.join(self.path, file) for file in os.listdir(self.path) if file.endswith('.xml')]
        self.input_data_to_mongodb(xml_files)

    def input_data_to_mongodb(self, decompressed_files):
        for file_path in tqdm(decompressed_files, desc="Uploading files", unit='iB', unit_scale=True):
            with open(file_path, mode='r', encoding='utf-8') as xml_file:
                xml_data = xml_file.read()

            json_data = xmltodict.parse(xml_data)
            self.insert_documents_bulk(json_data)

    def insert_documents_bulk(self, json_data):
        def extract_case_files(document):
            case_files = []
            def traverse_dict(d):
                if isinstance(d, dict):
                    for key, value in d.items():
                        if key == 'case-file':
                            if isinstance(value, list):
                                case_files.extend(value)
                            else:
                                case_files.append(value)
                        elif isinstance(value, (dict, list)):
                            traverse_dict(value)
                elif isinstance(d, list):
                    for item in d:
                        traverse_dict(item)
            
            traverse_dict(document)
            return case_files

        case_files = extract_case_files(json_data)

        # Bulk operations 리스트 생성
        bulk_operations = []

        for case_file in case_files:
            if isinstance(case_file, dict):
                serial_number = case_file.get('serial-number')
                registration_number = case_file.get('registration-number')
                
                if serial_number:
                    # MongoDB에 문서가 존재하는지 확인 후 업데이트 또는 삽입
                    bulk_operations.append(
                        UpdateOne(
                            {'_id': serial_number},
                            {'$set': case_file},
                            upsert=True
                        )
                    )

        if bulk_operations:
            # Bulk write 실행
            collection.bulk_write(bulk_operations)
                    
    def clean_up(self):
        for file_name in os.listdir(self.path):
            file_path = os.path.join(self.path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        print("XML : Cleanup completed.")