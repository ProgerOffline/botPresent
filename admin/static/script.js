let domen = "http://127.0.0.1:5000";

let buttons = document.querySelectorAll("#btn");
buttons[0].style.backgroundColor = "#295E3F";

let swithedButton = buttons[0];

buttons.forEach(element => {
    element.onclick = (e) => {
        if (e.srcElement.className == "button"){
            button = e.srcElement;
            button.style.backgroundColor = "#295E3F";
            button_text = button.textContent.trim();
    
            swithedButton.style.backgroundColor = "#74AB8B";
            swithedButton = button;
    
            show_data(button_text);
        } 
    }
});

function show_data(button_text) {
    if (button_text == "Клиенты"){
        show_clients_data();

    } else if (button_text == "Пополнения"){
        show_bills_data()

    } else if (button_text == "Вывод"){
        show_out_data();

    } else if (button_text == "Проценты"){
        show_precent_data();

    } else if (button_text == "Настройки"){
        show_settins_data();

    }
}

function show_clients_data() {
    let url = domen + "/api/getUsers";
    let connect = new XMLHttpRequest();
    connect.responseType = "json";
    connect.open("GET", url);
    connect.send();

    connect.onload = () => {
        result = connect.response;
        console.log(result);
        template = `
            <tr class="header">
                <td>ID</td>
                <td>Номер телефона</td>
                <td>Дата регистрации</td>
                <td>Кошелек PM</td>
                <td>Баланс</td>
                <td>Инвестиция</td>
            </tr>
        `;

        for(let i = 0; i < result.length; i++){
            template += `
                <tr class="user">
                    <td>${result[i].id}</td>
                    <td>${result[i].phone}</td>
                    <td>${result[i].reg_date}</td>
                    <td>${result[i].wallet}</td>
                    <td>${result[i].ballance}</td>
                    <td>${result[i].invest_amount}</td>
                </tr>
            `
        }

        document.getElementById("table-data").innerHTML = template;
    }
}

function show_bills_data() {

}

function show_out_data() {

}

function show_precent_data() {

}

function show_settins_data() {
    
}