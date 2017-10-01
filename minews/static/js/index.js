
console.log($);

$(document).ready(function() {
    console.log("enter document ready");
    grab_ithome();
});

function grab_ithome() {
    $.ajax({
        url: '/grab_ithome',
        method: 'get',
        success: function(data) {
            data = $.parseJSON(data);
            console.log(data);
            draw_result_table(data);
            pop_up_notification('有新消息哦', '您有新的消息，请查收');
            setTimeout('grab_ithome();', 30000);
        }
    });
}

function pop_up_notification(title, b) {
    if(window.Notification && Notification.permission !== "denied") {
        Notification.requestPermission(function(status) {    // 请求权限
            if(status === 'granted') {
                // 弹出一个通知
                var n = new Notification(title, {
                    body : b,
                    icon : $('#favicon_path').html(),
                });
                // 两秒后关闭通知
                setTimeout(function() {
                    n.close();
                }, 10000);
            }
        });
    }
}

function draw_result_table(d) {
    console.log('enter draw_result_table');
    $('#result_table').bootstrapTable('destroy');
    $('#result_table').bootstrapTable({
        columns: [{
            field: 'title',
            title: 'Title'
        }, {
            field: 'url',
            title: 'URL',
            formatter: url_link_formatter,
        }, {
            field: 'category',
            title: 'Category'
        }],
        // rowStyle: row_style_formatter,
        data: d,
    });
}

function row_style_formatter(row, index) {
    return {
        classes: 'text-nowrap another-class',
        css: {"color": "blue", "font-size": "50px"}
    };
}

function url_link_formatter(value, row, index) {
    return '<a target="_blank" href="' + value + '">' + value + '</a>'
}
