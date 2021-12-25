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
    }).then((response) => {
        // task_table.bootstrapTable('load', response);
        console.log('task_id:' + response);
        show_table(response);
        to_chart_button.attr('href', './chart/' + response);
        export_button.click(function (){
            this.file_export = file_export
            this.file_export('test.xlsx', './file/' + response);
        });
    }
    ).fail(() => {
        console.log('failed');
    })
}

function show_table(task_id) {
    var refresh_query = {
        url: 'http://127.0.0.1:8000/task/' + task_id,
        silent: true
        query: {
            'filter_switch': 1
        }
    }
    task_table.bootstrapTable('refresh', refresh_query);
}

function file_export(filename, url) {

    let link = document.createElement('a') //创建a标签
    link.style.display = 'none'  //使其隐藏
    link.href = url //赋予文件下载地址
    link.setAttribute('download', filename) //设置下载属性 以及文件名
    link.click() //强制触发a标签事件

    $(this).button('loading').delay(2000).queue(function() {
       $(this).button('reset');
       $(this).dequeue();
    });
}