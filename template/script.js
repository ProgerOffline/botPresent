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
    connect.responseType = JSON;
    connect.open(url, "GET");
    connect.send();

    connect.onload = () => {
        console.log(connect.response);
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