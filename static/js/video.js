function sendRequest(button) {
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
                 alert("合成路径是："+data);
            })
            .catch(error => console.error(error));
    }