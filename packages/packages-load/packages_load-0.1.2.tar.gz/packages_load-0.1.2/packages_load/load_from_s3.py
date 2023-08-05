import os.path
import requests
from pathlib import Path
import boto3
from fastapi import status


def read_pdf_from_s3(url, path_to_save):
    '''
    :param url: Name of packages_load bucket
    :parm path_to_save : place to save the pdf
    Downloads pdf file from packages_load
    '''
    try:
        bucket_name = url.split('//')[1].split('.')[0]
        filename = url.split('//')[1].split('/', 1)[1]
        session = boto3.Session()
        s3 = session.resource('s3')
        s3.Object(bucket_name, filename).download_file(os.path.join(path_to_save, filename.split('/')[-1]))

        return {
            "status_code": status.HTTP_200_OK,
            "message": "File downloaded",
            "filename": filename.split('/')[-1]
        }
    except Exception as e:
        return {
            "status_code": status.HTTP_400_BAD_REQUEST,
            "message": str(e)
        }


def download_signed_s3(url, path_to_save):
    try:
        r = requests.get(url)
        filename = url.split('//')[1].split('/')[-1].split(".pdf")[0]+".pdf"
        with open(path_to_save+"/"+filename, "wb") as code:
            code.write(r.content)

        return {
            "status_code": status.HTTP_200_OK,
            "message": "Downloaded successfully",
            "filename": filename
        }
    except Exception as e:
        return {"status_code": status.HTTP_400_BAD_REQUEST, "message": e}


def remove_directory(directory):
    '''
    :param directory: path to the directory which needs to be removed
    :return: removes input directory
    '''
    try:
        if os.path.exists(directory):
            directory = Path(directory)
            for item in directory.iterdir():
                if item.is_dir():
                    remove_directory(item)
                else:
                    item.unlink()
            directory.rmdir()

            return {
                "status_code": 200,
                "message": "Directory cleaned"
            }
    except Exception as e:
        return {
            "status_code": 400,
            "message": str(e)
        }


def load_from_s3(url, path_to_save):
    '''
    :param url: Takes input as the URL(signed or unsigned(object URL) from AWS S3
    :param path_to_save: path to save the pdf
    :return:
    '''
    if 'Signature' in url:
        signed_status = download_signed_s3(url=url, path_to_save=path_to_save)
    else:
        signed_status = read_pdf_from_s3(url=url, path_to_save=path_to_save)
    return signed_status

