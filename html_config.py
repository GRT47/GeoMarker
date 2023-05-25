def generate_popup_content(location):
    popup_content = f"""<div style='font-size: 16px; font-weight: bold;'>주소</div>
                        <div style='font-size: 14px;'>{location[2]}</div>
                        <div style='font-size: 16px; font-weight: bold;'>설명</div>
                        <div style='font-size: 14px;'>{location[3]}</div>
                        <div style='position: absolute; top: 5px; right: 173px;'>
                            <button style='
                                background-color: #4ca5af;
                                width: 70px;
                                height: 30px;
                                border: none;
                                color: black;
                                padding: 0px;
                                text-align: center;
                                text-decoration: none;
                                display: inline-block;
                                font-size: 16px;
                                font-weight: bold;
                                margin: 0px 0px;
                                cursor: pointer;
                            ' onclick="\
                                var dummy = document.createElement('input');\
                                document.body.appendChild(dummy);\
                                dummy.value = '{location[2]}';\
                                dummy.select();\
                                document.execCommand('copy');\
                                document.body.removeChild(dummy);\
                                alert('주소가 복사되었습니다.');\
                                ">주소복사</button>
                            </div>"""
    
    return popup_content

marker_list = None

def generate_marker_list(locations):
    global marker_list

    if marker_list is not None:
        return marker_list

    marker_list = "<div style='position: absolute; top: 10px; right: 10px; background-color: white; padding: 10px; z-index: 1000; width: 325px; height: 420px; display: none;' id='marker_list'>"
    marker_list += "<h3>빠른이동</h3>"
    marker_list += "<div style='overflow-y: scroll; max-height: 350px;'>"
    marker_list += "<ul style='list-style-type: none; padding: 0;'>"
    for i, location in enumerate(locations):
        address = location[2]
        nickname = location[3]
        marker_list += f"<li style='line-height: 2.5; cursor: pointer;' oncontextmenu='return false;' onclick='openPopup({i})'>{i + 1}. {address}</li>"
    marker_list += "</ul>"
    marker_list += "</div>"
    marker_list += "</div>"
    marker_list += "<button style='position: fixed; top: 10px; right: 10px; z-index: 1001; width: 100px; height: 50px; font-size: 20px; font-weight: bold; background-color: rgb(102, 102, 102); color: rgb(255, 255, 255);' onclick='toggleMarkerList()'>주소목록</button>"
    marker_list += "<script>"
    marker_list += "function toggleMarkerList() {"
    marker_list += "    var markerList = document.getElementById('marker_list');"
    marker_list += "    if (markerList.style.display === 'none') {"
    marker_list += "        markerList.style.display = 'block';"
    marker_list += "    } else {"
    marker_list += "        markerList.style.display = 'none';"
    marker_list += "    }"
    marker_list += "}"
    marker_list += "function openPopup(index) {"
    marker_list += "    var markers = document.getElementsByClassName('leaflet-marker-icon');"
    marker_list += "    var marker = markers[index];"
    marker_list += "    if (marker) {"
    marker_list += "        marker.click();"
    marker_list += "    }"
    marker_list += "}"
    marker_list += "</script>"

    return marker_list



