function show_edit(){
        const table = document.getElementById("my-table");
        table.setAttribute('contenteditable', true);
        const button_save = document.getElementById("save_data");
        button_save.style.display = "block";
        button_save.addEventListener("click", function() {
            // 获取表格数据
            const tableData = [];
            const rows = table.rows;
            for (let i = 0; i < rows.length; i++) {
                const rowData = [];
                const cells = rows[i].cells;
                for (let j = 0; j < cells.length; j++) {
                    rowData.push(cells[j].innerText);
                }
                tableData.push(rowData);
            }
            // 发送表格数据到后端进行保存
            fetch('/save', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(tableData)
            })
            .then(response => response.text())
            .then(data => {
                console.log(data);
                // 隐藏保存按钮
                button_save.style.display = "none";
                // 取消表格的可编辑状态
                table.setAttribute('contenteditable', false);
            })
            .catch(error => console.error(error));
        });
    }

