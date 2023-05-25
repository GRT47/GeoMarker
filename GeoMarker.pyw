from module import *

# 현재 파일의 경로를 가져와서 해당 경로의 폴더를 markers 폴더의 상위 폴더로 지정
current_path = os.path.dirname(os.path.abspath(__file__))
marker_folder = os.path.join(current_path, 'markers')

config = configparser.ConfigParser()
config.read('api_config.ini')
config.read('ftp_config.ini')  # INI 파일의 경로를 지정해야 합니다.

API_KEY = config.get('API', 'KEY')
url = config.get('url_setting', 'URL')
remote_url = config.get('Section', 'remote_url')

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('bar_icon.png'))
        self.show()

        self.setWindowTitle("지도만들기 Final_프로그램 외부공유금지!!!")
        self.resize(1000, 800)

        # 화면 중앙으로 위치시킴
        screen = QDesktopWidget().screenGeometry()
        self.move((screen.width() - self.width()) // 2, (screen.height() - self.height()) // 2)

        # QGridLayout 인스턴스 생성
        self.grid = QGridLayout()
        self.grid.setHorizontalSpacing(2)   # 그리드 셀 가로 간격 조절
        self.grid.setVerticalSpacing(2)     # 그리드 셀 세로 간격 조절
        self.grid.setColumnStretch(0, 1)   # 열 너비 조정
        self.grid.setColumnStretch(1, 1)
        self.grid.setColumnStretch(2, 1)

        # QLabel 위젯 생성 및 추가
        self.create_label()

        # QTableWidget 위젯 생성 및 추가
        self.create_table()

        # QPushButton 위젯 생성 및 추가
        self.create_buttons()

        # QProgressBar 위젯 생성 및 추가
        self.create_progress_bar()

        # QGridLayout 인스턴스를 self.setLayout()에 전달
        self.setLayout(self.grid)
        

    def create_label(self):
        label = QLabel(self)
        movie = QMovie("earth.gif")
        label.setMovie(movie)
        label.setFixedSize(70, 70)
        movie.setScaledSize(QSize(70, 70))
        movie.start()
        self.grid.addWidget(label, 2, 4, 2, 2)

    def create_table(self):
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["설명", "주소"])
        self.table.setRowCount(500)
        self.table.setColumnWidth(0, 600)
        self.table.setColumnWidth(1, 337)
        self.grid.addWidget(self.table, 0, 0, 2, 6)

    def create_buttons(self):
        button = QPushButton("지도저장")
        button.clicked.connect(self.search_location)
        button.setFont(QFont("맑은 고딕", 12, QFont.Bold))
        self.grid.addWidget(button, 2, 0)

        button_1 = QPushButton("지도공유")
        button_1.clicked.connect(self.share_location)
        button_1.setFont(QFont("맑은 고딕", 12, QFont.Bold))
        self.grid.addWidget(button_1, 2, 1)
        button_2 = QPushButton("지도 리스트")
        button_2.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(url)))
        button_2.setFont(QFont("맑은 고딕", 12, QFont.Bold))
        self.grid.addWidget(button_2, 2, 2)

    def create_progress_bar(self):
        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setAlignment(QtCore.Qt.AlignLeft)
        self.progress_bar.setFont(QtGui.QFont("맑은 고딕", 12, QtGui.QFont.Bold))
        self.progress_bar.setAlignment(Qt.AlignCenter)
        self.progress_bar.setStyleSheet("QProgressBar {background-color: #dddddd; border: 2px solid grey; border-radius: 5px; color: black;}"
                                        "QProgressBar::chunk {background-color: #38d14d; width: 20px; margin: 1px; font-weight: bold;}")
        self.grid.addWidget(self.progress_bar, 3, 0, 1, 4)

    def search_location(self):
        pass

    def share_location(self):
        pass

    def update_progress_bar(self, current, total):
        progress = int(current / total * 100)
        self.progress_bar.setValue(progress)
        self.progress_bar.setFormat(f"{progress}% ({current}/{total})")


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_V and event.modifiers() == Qt.ControlModifier:
            self.paste_clipboard_data()
        elif event.key() == Qt.Key_Delete:
            self.delete_selected_cells()

    def paste_clipboard_data(self):
         clipboard = QApplication.clipboard()
         data = clipboard.text()
         if data:
             rows = data.split('\n')
             for r, row in enumerate(rows[:-1]):
                 columns = row.split('\t')
                 for c, column in enumerate(columns):
                     new_item = QTableWidgetItem(column)
                     self.table.setItem(self.table.currentRow() + r, self.table.currentColumn() + c, new_item)

    def delete_selected_cells(self):
        cells = self.table.selectedItems()
        for cell in cells:
            self.table.setItem(cell.row(), cell.column(), QTableWidgetItem(""))

    # 지도저장 호출함수
    def search_location(self):
        addresses = []
        nicknames = []
        for row in range(self.table.rowCount()):
            address_item = self.table.item(row, 1)
            nickname_item = self.table.item(row, 0)  # 추가한 열에서 별명 정보를 가져옴
            if address_item is not None:
                address = address_item.text().strip()
                nickname = nickname_item.text().strip() if nickname_item is not None else ""
                if address:
                    addresses.append(address)
                    nicknames.append(nickname)

        locations = []
        total = len(addresses)
        current = 0
        not_found_count = 0
        for i, address in enumerate(addresses):
            url = "https://dapi.kakao.com/v2/local/search/address.json"
            headers = {"Authorization": f"KakaoAK {API_KEY}"}
            params = {"query": address}
            response = requests.get(url, headers=headers, params=params)
            current += 1
            self.update_progress_bar(current, total)
            if response.status_code == 200:
                data = json.loads(response.text)
                json.loads(response.text)
                if len(data["documents"]) > 0:
                    x = data["documents"][0]["x"]
                    y = data["documents"][0]["y"]
                    address = data["documents"][0]["address_name"].replace("\n", " ")
                    nickname = nicknames[i] if nicknames[i] else ""
                    locations.append((y, x, address, nickname))
                    if self.table.item(i, 1).background().color().name() == "#ffff00":
                        self.table.item(i, 1).setBackground(Qt.white)
                else:
                    not_found_count += 1
                    self.table.item(i, 1).setBackground(Qt.yellow)
                    self.table.item(i, 1).setToolTip("검색 결과가 없습니다.")
            else:
                error_message = f"{address}: 검색 중 오류가 발생했습니다. 상태 코드: {response.status_code}"
                QMessageBox.critical(self, "Error", error_message)
                print(error_message)

        if not_found_count > 0:
            QMessageBox.warning(self, "Warning", "일부 주소에 대한 검색 결과가 없습니다.")
        elif locations:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Map", ".", "HTML Files (*.html)")
            if file_path:
                map = folium.Map(location=locations[0][:2], zoom_start=13, tiles='https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
                  attr='Google', name='Google Map')
                for i, location in enumerate(locations):
                    popup_content = html_config.generate_popup_content(location)
                    marker_list = html_config.generate_marker_list(locations)
                    map.get_root().html.add_child(folium.Element(marker_list))
                    marker_file = os.path.join(marker_folder, f'number_{i+1}.png')
                    with open(marker_file, 'rb') as f:
                        data = base64.b64encode(f.read()).decode('utf-8')
                    icon_url = 'data:image/png;base64,' + data
                    icon = folium.features.CustomIcon(icon_url, icon_size=(30, 40))
                    alt_text = f'Marker {i+1}'
                    folium.Marker(location=location[:2], popup=folium.Popup(popup_content, max_width=249), icon=icon, alt=alt_text).add_to(map)

                map.save(file_path)
                webbrowser.open(file_path)
        else:
            QMessageBox.warning(self, "Warning", "모든 주소에 대한 검색 결과가 없습니다.")

    # 지도공유 호출함수
    def share_location(self):
        addresses = []
        nicknames = []
        for row in range(self.table.rowCount()):
            address_item = self.table.item(row, 1)
            nickname_item = self.table.item(row, 0)  # 추가한 열에서 별명 정보를 가져옴
            if address_item is not None:
                address = address_item.text().strip()
                nickname = nickname_item.text().strip() if nickname_item is not None else ""
                if address:
                    addresses.append(address)
                    nicknames.append(nickname)
        locations = []
        total = len(addresses)
        current = 0
        not_found_count = 0
        for i, address in enumerate(addresses):
            url = "https://dapi.kakao.com/v2/local/search/address.json"
            headers = {"Authorization": f"KakaoAK {API_KEY}"}
            params = {"query": address}
            response = requests.get(url, headers=headers, params=params)
            current += 1
            self.update_progress_bar(current, total)
            if response.status_code == 200:
                data = json.loads(response.text)
                json.loads(response.text)
                if len(data["documents"]) > 0:
                    x = data["documents"][0]["x"]
                    y = data["documents"][0]["y"]
                    address = data["documents"][0]["address_name"].replace("\n", " ")
                    nickname = nicknames[i] if nicknames[i] else ""
                    locations.append((y, x, address, nickname))
                    if self.table.item(i, 1).background().color().name() == "#ffff00":
                        self.table.item(i, 1).setBackground(Qt.white)
                else:
                    not_found_count += 1
                    self.table.item(i, 1).setBackground(Qt.yellow)
                    self.table.item(i, 1).setToolTip("검색 결과가 없습니다.")
            else:
                error_message = f"{address}: 검색 중 오류가 발생했습니다. 상태 코드: {response.status_code}"
                QMessageBox.critical(self, "Error", error_message)
                print(error_message)

        if not_found_count > 0:
            QMessageBox.warning(self, "Warning", "일부 주소에 대한 검색 결과가 없습니다.")
        elif locations:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Map", ".", "HTML Files (*.html)")
            if file_path:
                map = folium.Map(location=locations[0][:2], zoom_start=13, tiles='https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
                  attr='Google', name='Google Map')
                for i, location in enumerate(locations):
                    popup_content = html_config.generate_popup_content(location)
                    marker_list = html_config.generate_marker_list(locations)
                    map.get_root().html.add_child(folium.Element(marker_list))
                    marker_file = os.path.join(marker_folder, f'number_{i+1}.png')
                    with open(marker_file, 'rb') as f:
                        data = base64.b64encode(f.read()).decode('utf-8')
                    icon_url = 'data:image/png;base64,' + data
                    icon = folium.features.CustomIcon(icon_url, icon_size=(30, 40))
                    folium.Marker(location=location[:2], popup=folium.Popup(popup_content, max_width=249), icon=icon).add_to(map)
                map.save(file_path)
                try:
                    success = ftp_util.upload_to_ftp(file_path)
                    if success:
                        QMessageBox.information(self, "Information", "지도를 서버로 전송하엿습니다.")
                        print(remote_url)
                        file_name = os.path.basename(file_path)
                        url_to_open = remote_url + file_name
                        webbrowser.open(url_to_open)
                    else:
                        QMessageBox.warning(self, "Warning", "지도를 서버로 전송하는 중 오류가 발생했습니다.")
                except Exception as e:
                    QMessageBox.warning(self, "Warning", "지도를 서버로 전송하는 중 오류가 발생했습니다.")
                    print("Error:", e)
        else:
            QMessageBox.warning(self, "Warning", "모든 주소에 대한 검색 결과가 없습니다.")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 어두운 Fusion 스타일을 적용
    app.setStyle("Fusion")
    dark_palette = QtGui.QPalette()
    dark_palette.setColor(QtGui.QPalette.Window, QtGui.QColor(53, 53, 53))
    dark_palette.setColor(QtGui.QPalette.WindowText, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.Base, QtGui.QColor(224, 224, 224))
    dark_palette.setColor(QtGui.QPalette.AlternateBase, QtGui.QColor(53, 53, 53))
    dark_palette.setColor(QtGui.QPalette.ToolTipBase, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.ToolTipText, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.Text, QtCore.Qt.black)
    dark_palette.setColor(QtGui.QPalette.Button, QtGui.QColor(53, 53, 53))
    dark_palette.setColor(QtGui.QPalette.ButtonText, QtCore.Qt.white)
    dark_palette.setColor(QtGui.QPalette.BrightText, QtCore.Qt.red)
    dark_palette.setColor(QtGui.QPalette.Link, QtGui.QColor(42, 130, 218))
    dark_palette.setColor(QtGui.QPalette.Highlight, QtGui.QColor(42, 130, 218))
    dark_palette.setColor(QtGui.QPalette.HighlightedText, QtCore.Qt.black)
    app.setPalette(dark_palette)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())