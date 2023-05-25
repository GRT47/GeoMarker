<?php
$dir_path = 'map'; // 디렉토리 경로

// 파일 목록 가져오기 및 파일 수정시간 기준으로 정렬
$files = array();
foreach (scandir($dir_path) as $file) {
    $file_path = $dir_path.'/'.$file;
    if (is_file($file_path)) {
        $files[$file] = filemtime($file_path);
    }
}
if(isset($_GET['sort']) && $_GET['sort'] === 'desc') {
  arsort($files); // 파일 수정시간 내림차순으로 정렬
} else {
  asort($files); // 파일 수정시간 오름차순으로 정렬
}
$files = array_keys($files); // 정렬된 파일명 배열로 재설정

// Delete selected files
if (isset($_POST['delete_files'])) {
  $success_msg = [];
  $error_msg = [];

  foreach ($_POST['delete_files'] as $file) {
    $file_path = $dir_path . '/' . $file;

    if (file_exists($file_path) && unlink($file_path)) {
      $success_msg[] = $file;
    } else {
      $error_msg[] = $file;
    }
  }

  if (!empty($success_msg)) {
    echo '<script>alert("'.implode(", ", $success_msg).' 파일이 삭제되었습니다.");</script>';
  }

  if (!empty($error_msg)) {
    echo '<script>alert("'.implode(", ", $error_msg).' 파일을 삭제하는 중 오류가 발생했습니다.");</script>';
  }

  // Redirect to refresh page
  header("Location: ".$_SERVER['REQUEST_URI']);
  exit();
}


// Output file list and delete button
echo '<form id="file-list-form" method="post">';
echo '<div style="position: fixed; top: 0; right: 0; width: 100%; height:67; background-color: WHITE; border: 1px solid black; display: flex; flex-direction: row">';
echo '<div style="position: fixed; top: 1px; right: 441px;"><a href="?sort=asc" class="sort-btn">오름차순</a></div>';
//echo '<div style="width:20px"></div>';
echo '<div style="position: fixed; top: 1px; right: 341px;"><a href="?sort=desc" class="sort-btn">내림차순</a></div>';
echo '<div class="delete-btn" style="position: fixed; top: -20; right: 0;"><input type="submit" name="delete_all" style="position: relative" value="선택한 파일 삭제"></div>';
echo '<div class="select-btn" style="position: fixed; top: -20; right: 133;"><input type="button" name="select_all" style="position: relative" value="전체 선택" onclick="selectAllFiles();"></div>';
echo '</div>';
// 파일 리스트와 삭제 버튼 출력
echo '<div class="itemList" style="position: fixed;top: 30; overflow: auto; height: 95%; width:100%">';
echo '<table class="file-list">';
echo '<thead style="position: sticky; top: 0;"></th><th>파일 이름</th><th>생성 날짜<th><input type="checkbox" id="select-all-checkbox"></thead><tbody>'; // 체크박스 추가

foreach ($files as $file) {
  // Output file name, creation date, and delete checkbox
  echo '<tr>';
  echo '<td><a href="' . $dir_path . '/' . $file . '">' . $file . '</a></td>';
  echo '<td>' . date("Y-m-d H:i:s", filemtime($dir_path . '/' . $file)) . '</td>';
  echo '<td><input type="checkbox" name="delete_files[]" value="' . $file . '"></td></tr>';
}

echo '</tbody></table>';
echo '</form>';
echo '</div>';


// Output CSS styling
echo '
  <style>
    .file-list td a {
      text-decoration: none;
    }  
    .file-list {
      border-collapse: collapse;
      width: 100%;
    }
    .file-list th, .file-list td {
      border: 1px solid #ddd;
      padding: 8px;
      text-align: left;
    }
    .file-list th {
      background-color: #f2f2f2;
    }
    .delete-btn {
      text-align: right;
      margin-top: 16px;
    }
    .delete-btn input[type="submit"] {
      background-color: #f44336;
      color: #fff;
      border: none;
      padding: 8px 16px;
      border-radius: 4px;
      cursor: pointer;
    }
    .delete-btn input[type="submit"]:hover {
      background-color: #d32f2f;
    }
    .select-btn {
      text-align: right;
      margin-top: 16px;
    }
    .select-btn input[type="button"] {
      background-color: #f44336;
      color: #fff;
      border: none;
      padding: 8px 16px;
      border-radius: 4px;
      cursor: pointer;
    }
    .select-btn input[type="button"]:hover {
      background-color: #d32f2f;
    }
    .sort-btn {
      display: inline-block;
      background-color: #f44336;
      color: #fff;
      border: none;
      padding: 8px 1px;
      border-radius: 4px;
      cursor: pointer;
      text-decoration: none;
      font-size: 14px;
      width: 100px;
      height: 13px;
      text-align: center;
      line-height: 10px;
    }
    .sort-btn:hover {
      background-color: #d32f2f;
    }    
  </style>
';

// Output JavaScript for serializing form data and selecting all files
echo '
  <script>
    HTMLFormElement.prototype.serialize = function() {
      var inputs = [].slice.call(this.querySelectorAll(\'input[type=text], input[type=hidden], input[type=radio]:checked, select\'));
      return inputs.map(function(input) {
        return encodeURIComponent(input.name) + \'=\' + encodeURIComponent(input.value);
      }).join(\'&\');
    };

    function selectAllFiles() {
      var checkboxes = document.getElementsByName(\'delete_files[]\');
      var selectAllCheckbox = document.getElementById(\'select-all-checkbox\');
      
      selectAllCheckbox.checked = !selectAllCheckbox.checked; // 상태 반전

      for (var i = 0; i < checkboxes.length; i++) {
        checkboxes[i].checked = selectAllCheckbox.checked;
      }
    }

    // Update the "Select All" checkbox when individual checkboxes are clicked
    var checkboxes = document.getElementsByName(\'delete_files[]\');
    var selectAllCheckbox = document.getElementById(\'select-all-checkbox\');

    for (var i = 0; i < checkboxes.length; i++) {
      checkboxes[i].addEventListener(\'change\', function() {
        var allChecked = true;

        for (var j = 0; j < checkboxes.length; j++) {
          if (!checkboxes[j].checked) {
            allChecked = false;
            break;
          }
        }

        selectAllCheckbox.checked = allChecked;
      });
    }
  </script>
  
';


?>