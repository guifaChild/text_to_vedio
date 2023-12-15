function sendRequest(button) {
    $('#circle_reading').show();
     const textarea = document.getElementById("content_data");
      const text = textarea.value;
      const title = document.getElementById("title_video");
      const titletext = title.value;
      button.classList.add('loading');
      button.disabled = true;
        fetch('/single', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ content: text ,title :titletext})
            })
            .then(response => response.text())
            .then(data => {
                button.classList.remove('loading');
                 button.disabled = false;
                 $('#circle_reading').hide();
                 alert("合成路径是："+data);
                 showDetail(titletext);
            })
            .catch(error => console.error(error));

    }

function showDetail(title){
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        document.getElementById('container-fluid').innerHTML = xhr.responseText;
        console.log("查看行数据:");
      } else {
        console.error("查看行数据失败");
      }
    }
  };

  xhr.open("GET", "/show_detail?title="+title);
  xhr.send();
}
function deleteDetail(title){
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        document.getElementById('container-fluid').innerHTML = xhr.responseText;
        console.log("查看行数据:");
      } else {
        console.error("查看行数据失败");
      }
    }
  };

  xhr.open("GET", "/deleteDetail?title="+title);
  xhr.send();
}




function viewdetailContent(button){

    var currentRow = $(button).closest('tr');
    // 获取当前行中每个td的值
    var title = currentRow.find('td:eq(0)').text();
    var index = currentRow.find('td:eq(1)').text();
    var prompt = currentRow.find('td:eq(2)').text();
    var negative = currentRow.find('td:eq(3)').text();
     var image_path = currentRow.find('img').attr('src');

 $("#imagetext").val(title);
  $("#imageprompt").val(prompt);
   $("#imagenegitve").val(negative);
    $("#imagepath").attr("src", image_path);
     $("#hiddenValue").val(index);
}


function regenerateImage(){
const imageprompt = $("#imagetext").val();
const imagenegitve = $("#imageprompt").val();
const index = $("#hiddenValue").val();
var imgSrc = $("#imagepath").attr("src");
var titles = imgSrc.split('/');
var leng=titles.length;

var imagetitle = titles[leng-2];
  fetch('/regenerate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ imageprompt: imageprompt ,imagenegitve :imagenegitve,index:index,title:imagetitle})
            })
            .then(response => response.text())
            .then(data => {
                 var timestamp = new Date().getTime();
                 $("#imagepath").attr("src", imgSrc+ '?' + timestamp);
                $("#file_single tbody tr:eq(" + index + ") td:eq(4)").find("img").attr("src",imgSrc+ '?' + timestamp)
                alert("成功生成");



            })
            .catch(error => console.error(error));

}
function rebatchgenerateImage(){
const imageprompt = $("#imagetext").val();
const imagenegitve = $("#imageprompt").val();
const index = $("#hiddenValue").val();
var imgSrc = $("#imagepath").attr("src");
var titles = imgSrc.split('/');
var leng=titles.length;

var imagetitle = titles[leng-3];
var title  = titles[leng-2];


  fetch('/rebatchgenerate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ imageprompt: imageprompt ,imagenegitve :imagenegitve,index:index,title:title,filename:imagetitle})
            })
            .then(response => response.text())
            .then(data => {
                var timestamp = new Date().getTime();
                 $("#imagepath").attr("src", imgSrc+ '?' + timestamp);
                 // $("#imagepath").attr("src", image_path);  表格中也进行替换
                $("#file_single tbody tr:eq(" + index + ") td:eq(4)").find("img").attr("src",imgSrc+ '?' + timestamp)
                alert("成功生成");
            })
            .catch(error => console.error(error));
}

function remerge(image_path){

    fetch('/remerge', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ image_path: image_path })
            })
            .then(response => response.text())
            .then(data => {
                var timestamp = new Date().getTime();
                 $("#source_video").attr("src", imgSrc+ '?' + timestamp);
                alert("合成完成");
            })
            .catch(error => console.error(error));
}


