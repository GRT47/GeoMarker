import os
import configparser
from ftplib import FTP

def upload_to_ftp(file_path):
    # ftp_config.ini 파일 읽어오기
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'ftp_config.ini'))

    # FTP 접속 정보 가져오기
    host = config.get('FTP', 'HOST')
    username = config.get('FTP', 'USERNAME')
    password = config.get('FTP', 'PASSWORD')
    remote_path = config.get('FTP', 'REMOTE_PATH')

    try:
        ftp = FTP(host)
        ftp.login(username, password)
        ftp.cwd(remote_path)
        ftp.encoding = 'utf-8'
        ftp.sendcmd('OPTS UTF8 ON')   # 이 문구를 넣어줘야 한글 사용이 가능함 
        with open(file_path, 'rb') as f:
            ftp.storbinary('STOR ' + os.path.basename(file_path), f)
        ftp.quit()
        return True
    except Exception as e:
        print("Error:", e)
        return False