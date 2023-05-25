# utils.py

import sys
import webbrowser
import json
import requests
import folium
import base64
import os
import urllib.parse
import configparser
import ftp_util #ftp함수호출
import html_config #html구성
from ftplib import FTP
from PyQt5.QtCore import Qt, QSize, QUrl
from PyQt5.QtGui import QFont, QMovie, QIcon, QDesktopServices
from PyQt5.QtWidgets import (QApplication, QTableWidget, QTableWidgetItem, QPushButton, QWidget, QLabel,
                             QMessageBox, QProgressBar, QFileDialog, QDesktopWidget, QGridLayout)
from PyQt5 import QtGui, QtCore, QtWidgets
