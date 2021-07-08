const $ = django.jQuery;

function create_column(name, tag) {
    const th = document.createElement(tag);
    th.scope = 'col';
    th.innerHTML = name;
    return th;
}

function show_report() {

    const period = document.querySelector('#period').value;
    $.ajax({
        url: '/report_today_bs_api/',         /* Куда пойдет запрос */
        method: 'get',             /* Метод передачи (post или get) */
        dataType: 'json',          /* Тип данных в ответе (xml, json, script, html). */
        data: {period: period},     /* Параметры передаваемые в запросе. */
        success: function (result) {   /* функция которая будет выполнена после успешного запроса.  */
            // var data_spares = [] td - tr -
            const div_tag = document.getElementsByClassName('container-fluid myclasses')[0];
            if (div_tag.querySelector('table') != null){
                document.removeChild(div_tag);
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