

function loadContent(pageUrl) {
  // loadHeader(pageUrl);
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
          document.getElementById('content').innerHTML = xhr.responseText;
        // document.getElementById('container-fluid').innerHTML = xhr.responseText;
      } else {
        console.error('Failed to load page: ' + xhr.status);
      }
    }
  };
  xhr.open('GET', 'route?route='+pageUrl, true);
  xhr.send();

}

function loadroute(pageUrl) {
  // loadHeader(pageUrl);
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {

        document.getElementById('container-fluid').innerHTML = xhr.responseText;
      } else {
        console.error('Failed to load page: ' + xhr.status);
      }
    }
  };
  xhr.open('GET', 'route?route='+pageUrl, true);
  xhr.send();

}

function loadHeader(pageUrl) {
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {

        document.getElementById('content_header').innerHTML = xhr.responseText;
      } else {
        console.error('Failed to load page: ' + xhr.status);
      }
    }
  };
  xhr.open('GET', 'routeHeader?routeHeader='+pageUrl, true);
  xhr.send();
}
 function redirectToPage(pageUrl) {
        // 使用 window.location.href 实现页面跳转
        window.location.href = 'route?route='+pageUrl;
    }
