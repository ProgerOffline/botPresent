let domen = "http://62.109.24.170:5000";
let header = document.querySelector("header");
let saveButton = document.getElementById("btn-save");

function showErrorMessage() {
    new Toast({
        title: 'Ошибка',
        text: 'К сожелению данные не смогли дойти до сервера коректно, попробуйте перезагрузить страницу и повторить действия еще раз.',
        theme: 'danger',
        autohide: true,
        interval: 5000,
    });
}

function showSuccessMessage() {
    new Toast({
        title: 'Сохранение...',
        text: 'Данные успешно отправлены на сервер. Сервер их обработает в течении 5 минут. Спасибо за ожидание.',
        theme: 'success',
        autohide: true,
        interval: 5000,
    });
}

function getPicture() {
    let fileInput = document.getElementById("upload-file");
    
    if (fileInput == null) {
        return "Нет картинки";
    } else {
        let formData = new FormData();
        formData.append('file', fileInput.files[0]);

        return formData;
    }

}

function getData() {
    let table = document.getElementById("table-data");
    let rows = table.querySelectorAll("tr.user");
    let data = {};
    
    for (let i = 0; i < rows.length; i++){
        let paymentID = rows[i].getAttribute("payment-id");
        let outID = rows[i].getAttribute("out-id");
        let elements = rows[i].querySelectorAll("td");
        let list = [];

        for (let j = 0; j < elements.length; j++){
            try {
                let value = elements[j].querySelector("input").value;
                list.push(value);

            } catch (e) {
                try {
                    let value = elements[j]. querySelector("select").selectedOptions[0].label;
                    list.push(value);
                } catch (e) {
                    let value = elements[j].textContent;
                    list.push(value);
                }
            }
        }

        if (outID) {
            list.push(outID);
        }

        if (paymentID) {
            list.push(paymentID);
        }

        data[i] = list;
    }

    return data;
}

saveButton.onclick = () => {
    let type = saveButton.getAttribute("current-table");
    let url = domen + "/api/save/" + type;
    let data = JSON.stringify(getData());
    let picture = getPicture();

    $.ajax({
        type : "POST",
        url : url,
        data : { 'new-data' : data },
        success : showSuccessMessage,
        error : showErrorMessage,
    });

    $.ajax({
        url: domen + "/api/save/picture",
        type: 'POST',
        processData: false, // важно
        contentType: false, // важно
        dataType : 'json',
        data: picture,
    });
}

function showClients() {
    let url = domen + "/api/getUsers";
    let template = `
        <tr class="header">
            <td>ID</td>
            <td>Никнейм</td>
            <td>Номер телефона</td>
            <td>Дата регистрации</td>
            <td>Кошелек PM</td>
            <td>Баланс</td>
            <td>Инвестиция</td>
            <td>Доступ</td>
            <td></td>
        </tr>
    `;

    let connect = new XMLHttpRequest();
    connect.responseType = "json";
    connect.open("GET", url);
    connect.send();
    connect.onload = () => {
        result = connect.response;

        for(let i = 0; i < result.length; i++){
            template += `
                <tr class="user">
                    <td>${result[i].id}</td>
                    <td><input value='${result[i].username}'></input></td>
                    <td><input value='${result[i].phone}'></input></td>
                    <td><input value='${result[i].reg_date}'></input></td>
                    <td><input value='${result[i].wallet}'></input></td>
                    <td><input value='${result[i].ballance}'></input></td>
                    <td><input value='${result[i].invest_amount}'></input></td>
                    <td>
                        <select>
                            <option>${result[i].permission}</option>
                            <option>Открыт</option>
                            <option>Закрыт</option>
                        </select>
                    </td>
                    <td class="delete" onclick="deleteRecord(this)">Удалить</td>
                </tr>
            `;
        }

        saveButton.setAttribute("current-table", "clients");
        document.getElementById("header").innerHTML = "Клиенты";
        document.getElementById("table-data").innerHTML = template;
    }
}

function showPayements() {
    let url = domen + "/api/getPayments";
    let template = `
        <tr class="header">
            <td>ID</td>
            <td>Номер телефона</td>
            <td>Дата и время</td>
            <td>Банк</td>
            <td>Сумма, руб</td>
            <td>Статус</td>
            <td></td>
        </tr>
    `;

    let connect = new XMLHttpRequest();
    connect.responseType = "json";
    connect.open("GET", url);
    connect.send();
    connect.onload = () => {
        result = connect.response;
        for(let i = 0; i < result.length; i++){
            template += `
                <tr class="user" payment-id='${result[i].id}'>
                    <td>${result[i].user_db_id}</td>
                    <td><input value='${result[i].phone}'></input></td>
                    <td><input value='${result[i].date}'></input></td>
                    <td><input value='${result[i].bank}'></input></td>
                    <td><input value='${result[i].amount}'></input></td>
                    <td>
                        <select>
                            <option>${result[i].status}</option>
                            <option>Начислить</option>
                            <option>Отменить</option>
                        </select>
                    </td>
                    <td class="delete" onclick="deleteRecord(this)">Удалить</td>
                </tr>
            `;
        }

        saveButton.setAttribute("current-table", "payments");
        document.getElementById("header").innerHTML = "Пополнения";
        document.getElementById("table-data").innerHTML = template;
    }
}

function deleteRecord(element) {
    let parent = element.parentNode;
    let id;
    let type;
    let reloadData;

    if (parent.getAttribute("payment-id")) {
        id = parent.getAttribute("payment-id");
        type = "payment";
        reloadData = showPayements;
        
    } else {
        id = parent.children[0].textContent;
        type = "client";
        reloadData = showClients;
    }

    $.ajax({
        url : domen + "/api/delete/" + type,
        type: "POST",
        data: {"id" : id},
        success : reloadData,
        error : showErrorMessage,
    })
}
    
document.getElementById("btn-clients").onclick = () => {
    showClients();
}

document.getElementById("btn-payments").onclick = () => {
    showPayements();
}

document.getElementById("btn-settings").onclick = () => {
    let url = domen + "/api/getConstants";
    let template = `
        <tr class="header">
            <td>Текущий процент</td>
            <td>Реквизиты Сбербанка</td>
            <td>Реквизиты Тинькофф</td>
            <td>ФИО Сбербанк</td>
            <td>ФИО Тинькофф</td>
            <td>Кошелек PM</td>
            <td>PM Логин</td>
            <td>PM Пароль</td>
            <td>ID чата тех. поддержки</td>
        </tr>
    `;

    let connect = new XMLHttpRequest();
    connect.responseType = "json";
    connect.open("GET", url);
    connect.send();
    connect.onload = () => {
        result = connect.response;
        template += `
            <tr class="user">
                <td><input value='${result.precent}'></input></td>
                <td><input value='${result.cber_bank}'></input></td>
                <td><input value='${result.tinkoff_bank}'></input></td>
                <td><input value='${result.fio_cber}'></input></td>
                <td><input value='${result.fio_tinkoff}'></input></td>
                <td><input value='${result.wallet_pm}'></input></td>
                <td><input value='${result.pm_account}'></input></td>
                <td><input value='${result.pm_passwd}'></input></td>
                <td><input value='${result.support_chat_id}'></input></td>
            </tr>
            <tr class='file-upload'>
                <td>Прикрепить фото</td>
            </tr>
            <tr style='width: 300px'>
                <td style='padding: 10px'><input id='upload-file' type='file'></input></td>
            </tr>
        `;

        saveButton.setAttribute("current-table", "settings");
        document.getElementById("header").innerHTML = "Настройки";
        document.getElementById("table-data").innerHTML = template;
    }
}

document.getElementById("btn-out").onclick = () => {
    let url = domen + "/api/getOuts";
    let template = `
        <tr class="header">
            <td>ID</td>
            <td>Номер телефона</td>
            <td>Дата и время</td>
            <td>Кошелек PM</td>
            <td>Сумма $</td>
            <td>Ошибка</td>
        </tr>
    `;

    let connect = new XMLHttpRequest();
    connect.responseType = "json";
    connect.open("GET", url);
    connect.send();
    connect.onload = () => { 
        result = connect.response;

        for(let i = 0; i < result.length; i++){
            template += `
                <tr class="user" out-id="${result[i].id}">
                    <td>${result[i].user_db_id}</td>
                    <td>${result[i].phone}</td>
                    <td>${result[i].date}</td>
                    <td>${result[i].wallet}</td>
                    <td>${result[i].amount}</td>
                    <td >${result[i].error}</td>
                </tr>
            `;
        }

        saveButton.setAttribute("current-table", "");
        document.getElementById("header").innerHTML = "Выводы";
        document.getElementById("table-data").innerHTML = template;
    }
}
