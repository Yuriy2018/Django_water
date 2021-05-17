var posits;
var positions_M;
function get_ajax(){

// Создаём объект класса XMLHttpRequest
const request = new XMLHttpRequest();

/*  Составляем строку запроса и кладем данные, строка состоит из:
пути до файла обработчика ? имя в GET запросе где будет лежать значение запроса id_product и
через & мы передаем количество qty_product. */
const url = "/api/positions/";

/* Здесь мы указываем параметры соединения с сервером, т.е. мы указываем метод соединения GET,
а после запятой мы указываем путь к файлу на сервере который будет обрабатывать наш запрос. */
request.open('GET', url);

// Указываем заголовки для сервера, говорим что тип данных, - контент который мы хотим получить должен быть не закодирован.
request.setRequestHeader('Content-Type', 'application/x-www-form-url');

// Здесь мы получаем ответ от сервера на запрос, лучше сказать ждем ответ от сервера
    //let posits;
request.addEventListener("readystatechange", () => {

 /*   request.readyState - возвращает текущее состояние объекта XHR(XMLHttpRequest) объекта,
 бывает 4 состояния 4-е состояние запроса - операция полностью завершена, пришел ответ от сервера,
 вот то что нам нужно request.status это статус ответа,
 нам нужен код 200 это нормальный ответ сервера, 401 файл не найден, 500 сервер дал ошибку и прочее...   */

    if (request.readyState === 4 && request.status === 200) {

       posits = JSON.parse(request.responseText);
	    // выводим в консоль то что ответил сервер
	  console.log( posits);
    }
});

// Выполняем запрос
  request.send();
return posits;
}


console.log('sd')

function add_event(index_row){
    let elem = document.querySelector('#id_tabulars-'+index_row+'-position');

    elem.addEventListener('change', function() {
        number_pos = elem.value
        price = posits[number_pos-1].price
        quantity = document.querySelector("#id_tabulars-"+index_row+"-quantity").value
        if (quantity == '0') {
            quantity = 1;
        }
        document.querySelector("#id_tabulars-"+index_row+"-price").value = price
        document.querySelector("#id_tabulars-"+index_row+"-quantity").value = quantity
        document.querySelector("#id_tabulars-"+index_row+"-amount").value = price * quantity;


    });

    let elem_price = document.querySelector('#id_tabulars-'+index_row+'-price');

    elem_price.addEventListener('change', function() {
        number_pos = elem.value
        price = document.querySelector("#id_tabulars-"+index_row+"-price").value
        quantity = document.querySelector("#id_tabulars-"+index_row+"-quantity").value
        if (quantity == '0') {
            quantity = 1;
        }
        //document.querySelector("#id_tabulars-"+index_row+"-price").value = price
        //document.querySelector("#id_tabulars-"+index_row+"-quantity").value = quantity
        document.querySelector("#id_tabulars-"+index_row+"-amount").value = price * quantity;


    });

    let elem_quantuty = document.querySelector('#id_tabulars-'+index_row+'-quantity');

    elem_quantuty.addEventListener('change', function() {
        price = document.querySelector("#id_tabulars-"+index_row+"-price").value
        quantity = document.querySelector("#id_tabulars-"+index_row+"-quantity").value
        document.querySelector("#id_tabulars-"+index_row+"-amount").value = price * quantity;


    });
}

(function($) {
    $(document).on('formset:added', function(event, $row, formsetName) {
        if (formsetName == 'tabulars') {
            // Do something
            var row_ind = $row.prevObject.get()[0].previousElementSibling.rowIndex
            add_event(row_ind-1)
            console.log('Добавлена строка номер: ' + row_ind)
        }
    });

    $(document).on('formset:removed', function(event, $row, formsetName) {
        // Row removed
        console.log('Row removed!')
    });
})(django.jQuery);


document.addEventListener("DOMContentLoaded", function() {

	positions_M = get_ajax()
    console.log("Загружена страница!")
});