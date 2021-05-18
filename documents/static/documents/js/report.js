function take_ajax(){

    //	Данные для передачи на сервер например	id товаров и его количество
let id_product = 321;
let qty_product = 2;

 // принцип	тот же самый что и у обычного POST	запроса
const request = new XMLHttpRequest();
const url = "/api/procces_order/";
const params = "id_product=" + id_product+ "&qty_product=" + qty_product;

//	Здесь нужно указать в каком формате мы будем принимать данные вот и все	отличие
request.responseType =	"json";
request.open("POST", url, true, 'yuriy', '123');
request.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

request.addEventListener("readystatechange", () => {

    if (request.readyState === 4 && request.status === 200) {
        let obj = request.response;

	console.log(obj);
	// Здесь мы можем обращаться к свойству объекта и получать	его значение
	console.log(obj.id_product);
	console.log(obj.qty_product);
	}
});

request.send(params);

}

function event_for_start(){
    // document.querySelectorAll("button")[0].parentElement.parentElement.querySelector('.hidden').innerText
    document.querySelectorAll('button').forEach(function (el, i) {

        var id_order = el.parentElement.parentElement.querySelector('.hidden').innerText
        console.log(id_order)

        var delivered = el.parentElement.parentElement.querySelector('.delivered').checked
        var postponed = el.parentElement.parentElement.querySelector('.postponed').checked


    // let elem = document.querySelector('#id_' + el.name);
    //
    // elem.addEventListener('change', function() {
    //     number_pos = elem.value
    //     price = posits[number_pos-1].price
    //     quantity = document.querySelector("#id_" + el.name.replace('position','quantity')).value
    //     document.querySelector("#id_" + el.name.replace('position','amount')).value = price * quantity;
    //
    // });

}     )};

document.addEventListener("DOMContentLoaded", function() {
    console.log("Загружена страница!")
    event_for_start()
    take_ajax()
});

