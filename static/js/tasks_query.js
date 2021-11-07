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

function task_query() {
    console.log('button click');

    var start_date = setting_date_start.val();
    var end_date = setting_date_end.val();
    console.log(start_date + ' ' + end_date);

    console.log('')
    data = {
        "start_date": start_date,
        "end_date": end_date,
        "filters": ["a"]
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
    }
    ).fail(() => {
        console.log('failed');
    })
}