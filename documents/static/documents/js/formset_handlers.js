var posits;
var positions_M;
var task = null;
const $ = django.jQuery;
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

function get_amount(){

    if (document.querySelector("#order_form > div > fieldset > div.form-row.field-amount > div > div") != null) {
    var sum_dok = 0;
    document.querySelectorAll('.field-amount input').forEach(function (el, i) {
        if (el.name != 'amount'){
            sum_dok += Number(el.value)
        }
        })
    console.log(sum_dok)
    document.querySelector("#order_form > div > fieldset > div.form-row.field-amount > div > div").innerText = sum_dok
}};

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
        get_amount();

    });

    let elem_price = document.querySelector('#id_tabulars-'+index_row+'-price');

    elem_price.addEventListener('change', function() {
        number_pos = elem.value
        price = document.querySelector("#id_tabulars-"+index_row+"-price").value
        quantity = document.querySelector("#id_tabulars-"+index_row+"-quantity").value
        if (quantity == '0') {
            quantity = 1;
        }
        document.querySelector("#id_tabulars-"+index_row+"-amount").value = price * quantity;
        get_amount();

    });

    let elem_quantuty = document.querySelector('#id_tabulars-'+index_row+'-quantity');

    elem_quantuty.addEventListener('change', function() {
        price = document.querySelector("#id_tabulars-"+index_row+"-price").value
        quantity = document.querySelector("#id_tabulars-"+index_row+"-quantity").value
        document.querySelector("#id_tabulars-"+index_row+"-amount").value = price * quantity;
        get_amount();

    });

    get_amount();
}

(function($) {
    $(document).on('formset:added', function(event, $row, formsetName) {
        if (formsetName == 'tabulars') {
            // Do something
            var row_ind = $row.prevObject.get()[0].previousElementSibling.rowIndex
            add_event(row_ind-1)
            console.log('Добавлена строка номер: ' + row_ind)
            //someWork();
        }
    });

    $(document).on('formset:removed', function(event, $row, formsetName) {
        // Row removed
        get_amount();
        console.log('Row removed!')
    });
})(django.jQuery);


function add_event_for_start(){

    document.querySelectorAll('.field-position .related-widget-wrapper select').forEach(function (el, i) {
        if (el.name == 'tabulars-__prefix__-position') {
            console.log('Continue')

        } else  {


    let elem = document.querySelector('#id_' + el.name);

    elem.addEventListener('change', function() {
        number_pos = elem.value
        price = posits[number_pos-1].price
        quantity = document.querySelector("#id_" + el.name.replace('position','quantity')).value
        if (quantity == '0') {
            quantity = 1;
        }
        document.querySelector("#id_" + el.name.replace('position','price')).value = price
        document.querySelector("#id_" + el.name.replace('position','quantity')).value = quantity
        document.querySelector("#id_" + el.name.replace('position','amount')).value = price * quantity;
        get_amount();

    });

    let elem_price = document.querySelector("#id_" + el.name.replace('position','price'));

    elem_price.addEventListener('change', function() {
        number_pos = elem.value
        price = document.querySelector("#id_" + el.name.replace('position','price')).value
        quantity = document.querySelector("#id_" + el.name.replace('position','quantity')).value
        if (quantity == '0') {
            quantity = 1;
        }
        document.querySelector("#id_" + el.name.replace('position','amount')).value = price * quantity;
        get_amount();

    });

    let elem_quantuty = document.querySelector("#id_" + el.name.replace('position','quantity'));

    elem_quantuty.addEventListener('change', function() {
        price = document.querySelector("#id_" + el.name.replace('position','price')).value
        quantity = document.querySelector("#id_" + el.name.replace('position','quantity')).value
        document.querySelector("#id_" + el.name.replace('position','amount')).value = price * quantity;
        get_amount();

    });

    get_amount();
}    } )


};

function someWork() {
    task = null;

    $('.admin-autocomplete').on('change',function () {

       // client_str = document.querySelector("#id_client").innerText
              // создаем AJAX-вызов
    //     $.ajax('/get_driver_client/', {text : client_str}).done(function (result) {
    //      // alert('Сработал обработчик на jquery!');
    // })
    // var client_str = '';
    $.ajax({
		url: '/api/get_driver_client/',
		type: 'POST',
		dataType: 'json',
		data: {id: document.querySelector("#id_client").value, csrfmiddlewaretoken : csrftoken},
		success: function(data){
			// alert(data);
			let parent = document.querySelector('.field-client');
			if (document.querySelector(".field-client p") == null) {
                let p = document.createElement('p');
                p.innerHTML = "<div class='textdriver' style='margin-left: 500px; margin-top: 5px; color: #5b80b2; font-size: medium'>" + "   " + data.data.text + "</div>";
                parent.appendChild(p)
            } else {
			    document.querySelector(".field-client p .textdriver").innerText = data.data.text ;
            }
		    // $('#message').html(data);
		}
	});
    //     var formData = $( this ).serialize();
    //     $.post( "/api/get_driver_client/", formData, function( data ) { //  передаем и загружаем данные с сервера с помощью HTTP запроса методом POST
	//       // $( "div" ).html( data ); // вставляем в элемент <div> данные, полученные от сервера
    //         alert(data);
	//     })
    //
    });

}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

document.addEventListener("DOMContentLoaded", function() {

	positions_M = get_ajax()
    add_event_for_start()
    // $('')
    console.log("Загружена страница!")
    if (task !== null) {
        clearTimeout(task);
        task = null;
    }
    // Запускаем новый таймер
    task = setTimeout(someWork, 2000);

});