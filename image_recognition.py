import dataclasses
import os
import easyocr
from os.path import exists
import hashlib
import pickle


@dataclasses.dataclass
class DocumentData:
    bank_id: str
    inn: str
    acc: str
    corr_acc: str
    total: str


cache_path: str = 'cache/'


def first_item(arr: list):
    try:
        return arr[0]
    except IndexError:
        return None


def hash_file(file) -> str:
    h = hashlib.sha1()
    chunk = None
    while chunk != b'':
        chunk = file.read(1024)
        h.update(chunk)
    file.seek(0)
    return h.hexdigest()


def recognize_image(file, output_path: str):
    reader = easyocr.Reader(['ru'], verbose=False)
    result: list[str] = reader.readtext(file.read(), detail=0)
    file.seek(0)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as file:
        pickle.dump(result, file)


def parse_recognition(result: list[str]) -> DocumentData:
    numbers = [x for x in result if x.isdigit()]
    bank_id = first_item([x for x in numbers if x[0] == '0' and len(x) == 9])
    inn = first_item([x for x in numbers if len(x) == 12 and x.isdigit()])
    acc = first_item([x for x in numbers if x[0] == '4' and len(x) == 20])
    corr_acc = first_item([x for x in numbers if x[0] == '3' and len(x) == 20])
    total = first_item([x for x in result if ',00' in x])
    if total is not None:
        total = total.replace(',00', '').replace(' ', '')
    return DocumentData(bank_id, inn, acc, corr_acc, total)


def process_file(file) -> DocumentData:
    hash_data: str = hash_file(file)
    hash_path: str = cache_path + hash_data
    if not exists(hash_path):
        recognize_image(file, hash_path)
    with open(hash_path, 'rb') as cached_file:
        document_data: DocumentData = parse_recognition(pickle.load(cached_file))
    return document_data


def main():
    file_path = 'media/test.png'
    with open(file_path, 'rb') as file:
        print(process_file(file))


if __name__ == '__main__':
    main()
