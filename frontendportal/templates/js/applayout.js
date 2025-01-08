let routes = {{ routesJsonList }};

$(".applyout-center-panel-tabs").tabs({
    onSelect: function(title,index) {
        for (var i=0; i < routes.length; i++) {
            if (i == index) {
                console.log(routes[i].id);
                applayoutLoadRouteContent(routes[i].url, routes[i].id);
                return;
            }
        }
    }
});


function applayoutLoadRouteContent(url, contentElementId)
{
    $.ajax({
        type: 'get',
        url: url,
        async: true,
        beforeSend: function() {
            //Upload progress
            showProgress('{{ _("Progression...") }}', '{{ _("Please wait") }}');
        },
        data: '',
        error: function(data){
            closeProgress();
        },
        success:function(data, status){
            closeProgress();
            if (data.status == "OK") {
                $("#"+contentElementId).html(data.html);
                eval(data.js);
            } else if (data.status == "ERROR" && data.status_code == "000") {
                $.messager.alert({
                    title: data.status,
                    msg: data.message,
                    fn: function(){
                        window.location = '{{ url_for("auth.index") }}';
                    }
                });
            } else {
                $.messager.alert({
                    title: data.status,
                    msg: data.message,
                    fn: function(){
                        
                    }
                });
            }
        },
    });
}

function applayoutLogOut() {
    $.messager.confirm({
        title: "{{_('Confirm to sign Out')}}",
        msg: "{{_('Are you sure you would like to sign out')}}",
        fn: function(r){
            if (r){
                $.ajax({
                    type: 'post',
                    url: '{{ url_for("auth.logout") }}',
                    async: true,
                    beforeSend: function() {
                         //Upload progress
                        showProgress('{{ _("Progression...") }}', '{{ _("Please wait") }}');
                    },
                    data: '',
                    error: function(data){
                        closeProgress();
                        console.log(data.responseText);
                    },
                    success:function(data, status){
                        closeProgress();
                        if (data.status == "OK") {
                            window.location = '{{ url_for("auth.index") }}';
                            console.log(data.responseText);
                        } else {
                            $.messager.alert({
                                title: data.status,
                                msg: data.message,
                                fn: function(){
                                    //...
                                }
                            });
                        }
                    },
                });
            }
        }
    });
}