

function loadContent(pageUrl) {
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
    if (xhr.readyState === XMLHttpRequest.DONE) {
      if (xhr.status === 200) {
        document.getElementById('content').innerHTML = xhr.responseText;
      } else {
        console.error('Failed to load page: ' + xhr.status);
      }
    }
  };
  xhr.open('GET', pageUrl, true);
  xhr.send();
}




