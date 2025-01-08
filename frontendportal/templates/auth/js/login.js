$( document ).ready(function() {
    
    var sacco_id_elem = $("#auth_login_panel_form_sacco_id");
    var phone_or_email_elem=$("#auth_login_panel_form_phone_or_email")
    var password_elem = $("#auth_login_panel_form_password");
    var submit_button_elem = $("#auth_login_panel_form_submit_button");
    
    
    sacco_id_elem.textbox('textbox').bind('keydown', function(e){
        console.log(e);
        if (e.keyCode == 13){	// when press ENTER key, accept the inputed value.
            loginSubmitForm();
        }
    });

    
    phone_or_email_elem.textbox('textbox').bind('keydown', function(e){
        console.log(e);
        if (e.keyCode == 13){  // when press ENTER key, accept the inputed value.
            loginSubmitForm();
        }
    });
    
    password_elem.textbox('textbox').bind('keydown', function(e){
        if (e.keyCode == 13){	// when press ENTER key, accept the inputed value.
            loginSubmitForm();
        }
    });

    
    submit_button_elem.linkbutton({
        onClick: function() {
            loginSubmitForm();
        }
    });

    function loginSubmitForm()
    {
        if (!$("#auth_login_panel_form").form('validate')) {
            alert("Form is invalid");
            return;
        }
        
        showProgress('{{ _("Progression...") }}', '{{ _("Please wait") }}');
        $("#auth_login_panel_form").form('submit', {
            url: '{{ url_for("auth.authenticate") }}',
            method: 'post',
            success: function(data) {
                closeProgress();
                var data = eval('(' + data + ')');  // change the JSON string to javascript object
                if (data.status != "OK"){
                    $.messager.alert({
                        title: data.status,
                        msg: data.message,
                        fn: function(){
                            //...
                        }
                    });
                } else {
                    $.messager.show({
                        title: data.status,
                        msg:data.message,
                        timeout:3000,
                        showType:'slide'
                    });
                    setTimeout(function(){
                        window.location = "{{ url_for('applayout.applayout')}}";
                    },1000);
                }
            }
        });
    }

});


