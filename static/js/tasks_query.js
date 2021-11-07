const setting_date = $('#sandbox-container .input-daterange');
setting_date.datepicker({
    daysOfWeekHighlighted: "0,6",
    autoclose: true,
    todayHighlight: true
});
const setting_date_start = $('#sandbox-container .input-daterange .start');
setting_date_start.datepicker('update', new Date());

const setting_date_end = $('#sandbox-container .input-daterange .end');
setting_date_end.datepicker('update', new Date());

const task_table = $('#task_table');

const to_chart_button = $('#to_chart_button');

function task_query() {
    console.log('button click');

    var from_date = setting_date_start.val();
    var to_date = setting_date_end.val();

    var checked_list = []

    $('.form-check .form-check-input:checked').each(
        (index, obj) => {
            checked_list.push(obj.value)
        }
    )

    console.log(checked_list)
    data = {
        "from_date": from_date,
        "to_date": to_date,
        "filters": checked_list
    }

    json_data = JSON.stringify(data)
    $.post({
        url: "http://127.0.0.1:8000/task_query/",
        contentType: "application/json",
        data: json_data
    }
    ).then((response) => {
        // task_table.bootstrapTable('load', response);
        console.log(response);
        var refresh_query = {
            url: 'http://127.0.0.1:8000/task/' + response,
            silent: true
        }
        task_table.bootstrapTable('refresh', refresh_query);
        to_chart_button.attr('href', './chart/' + response);

    }
    ).fail(() => {
        console.log('failed');
    })
}