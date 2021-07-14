// const $ = django.jQuery;
var $j = jQuery.noConflict();
// $j("#datepicker").datepicker();

var months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

$j("#datepicker").datepicker({
    dateFormat: 'dd/mm/yy',
    monthNames: months,
    maxDate: '0',
            });

$j("#datepicker2").datepicker({
    dateFormat: 'dd/mm/yy',
    monthNames: months,
    maxDate: '0',
            });

function show_report() {

    var reports = document.getElementById('type_report');
    if (reports.value == '1') {
        show_waybill()
    }
    else if (reports.value == '2') {
        // show_orders()
        show_main('/report_orders_bs_api/',null)
    }
    else if (reports.value == '3') {
        // show_orders()
        show_main('/report_new_clients_bs_api/',null)
    }
    else if (reports.value == '4') {
        // show_orders()
        var pos = document.getElementById('positions');
        var positions = {'position':pos.value}
        show_main('/report_for_position_bs_api/',positions)
    }
    else if (reports.value == '5') {
        show_main('/report_analysis_clients/',null)
    }

    // const period = document.querySelector('#period').value;

}

function show_waybill() {

    // $('#period').find('option').remove();
    // $('#period').append('<option value="1" selected="selected">17:30-08:30</option>');
    // $('#period').append('<option value="2" selected="selected">08:30-17:30</option>');
    //
    // document.querySelector('div #orders').style.color = 'grey'
    // document.querySelector('div #waybill').style.color = 'black'
     const period = document.querySelector('#period').value;
     $j.ajax({
        url: '/report_today_bs_api/',         /* Куда пойдет запрос */
        method: 'get',             /* Метод передачи (post или get) */
        dataType: 'json',          /* Тип данных в ответе (xml, json, script, html). */
        data: {period: period},     /* Параметры передаваемые в запросе. */
        success: function (result) {   /* функция которая будет выполнена после успешного запроса.  */
            // var data_spares = [] td - tr -
            const div_tag = document.getElementsByClassName('container-fluid myclasses')[0];
            // if (div_tag.querySelector('table') != null){
            //     document.removeChild(div_tag);
            // };

            while (div_tag.firstChild) {
                div_tag.removeChild(div_tag.firstChild)
            };


            for (const table_line of result['list_tabls']) {
                const h4 = document.createElement('H4');
                h4.innerHTML = 'Путевой лист: ' + table_line['driver']
                div_tag.appendChild(h4);

                const table = document.createElement('table');
                table.className = 'table table-bordered'

                const thead = document.createElement('thead');
                thead.innerHTML = result['thead'];
                table.appendChild(thead);

                let tbody = document.createElement('tbody');
                tbody.innerHTML = table_line['str_tbody'];
                table.appendChild(tbody);
                div_tag.appendChild(table)

            }

        }
    });
}


function show_main(url,additional) {

    const datapicker = document.querySelector('.datapicker').value;
    const datapicker2 = document.querySelector('div #datepicker2').value;
    var data = {start: datapicker, finish: datapicker2}
    if (additional != null) {
        data['position'] = additional.position;
    }
    $j.ajax({
        url: url,         /* Куда пойдет запрос */
        method: 'get',             /* Метод передачи (post или get) */
        dataType: 'json',          /* Тип данных в ответе (xml, json, script, html). */
        data: data,     /* Параметры передаваемые в запросе. */
        success: function (result) {   /* функция которая будет выполнена после успешного запроса.  */
            const div_tag = document.getElementsByClassName('container-fluid myclasses')[0];

            while (div_tag.firstChild) {
                div_tag.removeChild(div_tag.firstChild)
            };

                const h4 = document.createElement('H4');
                h4.innerHTML = result['header_report']
                div_tag.appendChild(h4);

                const table = document.createElement('table');
                table.className = 'table table-bordered'

                const thead = document.createElement('thead');
                thead.innerHTML = result['thead'];
                table.appendChild(thead);

                let tbody = document.createElement('tbody');
                tbody.innerHTML = result['str_tbody'];
                table.appendChild(tbody);
                div_tag.appendChild(table)

        }
    });
}


function for_open(){
    var reports = document.getElementById('type_report');
    var datepicker = document.getElementById('datepicker')
    var datepicker2 = document.getElementById('datepicker2')
    var period = document.getElementById('period')
    var positions = document.getElementById('positions')

    if (reports.value == '1') {
        datepicker.hidden = true;
        datepicker2.hidden = true;
        positions.hidden = true;
        period.hidden = false;
    }
    else {
        datepicker.hidden = false;
        datepicker2.hidden = false;
        period.hidden = true;
        positions.hidden = true;
    }

     if (reports.value == '4') {
        positions.hidden = false;
    }
    console.log(reports)
}

window.onload = function() {
    // alert('load')
    for_open()
}