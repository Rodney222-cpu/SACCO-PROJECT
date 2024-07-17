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