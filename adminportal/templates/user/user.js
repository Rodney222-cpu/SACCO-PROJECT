

$("#user_html_table").datagrid({
    url: '{{ url_for("user.getUser") }}',
    toolbar: '#user_html_table_toolbar',
    fit:true,
    pagination: true,
    rownumbers: true,
    columns: [[
        {field:'id', title:'ID',width:'5%'},
        {field:'name', title:'{{ _('Name') }}',width:'15%'},
        {field:'phone', title:'{{ _('Phone') }}',width:'12%'},
        {field:'email', title:'{{ _('Email') }}',width:'18%'},
        {field:'created_on', title:'{{ _('Created On') }}',width:'20%'},
        {field:'updated_on', title:'{{ _('Updated On') }}',width:'20%'},
        {field:'options', title:'{{ _('Options') }}', width:'15%',
            formatter: function(value,row,index) {
                console.log(row);
                return '<a href="#" class="label-anchor" onclick="global_functions.userLaunchUpdateDialog(\''+index+'\');">Edit</a>';
            }
        }
    ]]
});

global_functions.userLaunchUpdateDialog = function(index) {
    var dataRows = $("#user_html_table").datagrid("getData");
    global_functions.userAddNewUser(dataRows.rows[index]);
}

$("#user_html_table_toolbar_new_button").linkbutton({ 
    onClick: function () {
        global_functions.userAddNewUser({});
    }
});

$("#user_html_table_toolbar_update_button").linkbutton();

$("#user_html_table_toolbar_delete_button").linkbutton(
    {
        onClick: function () {
            global_functions.userDeleteUser({});
        }
    }
);


    global_functions.userDeleteUser = function() {
        
        var rows = $("#user_html_table").datagrid('getSelections');
        if (rows.length < 1) {
            $.messager.alert('{{ _("Error") }}', '{{ _("Please select a USER to delete.") }}', 'error');
            return;
        }
        
        $.messager.confirm(
            '{{ _("Confirm") }}', '{{ _("Are you sure you want to delete this USER?") }}', 
            function(r){
                if (r){
                    $.ajax({
                        url: '{{ url_for("user.deleteUser") }}',
                        type: 'POST',
                        data: JSON.stringify(rows),
                        dataType: 'json',
                        headers: {"Content-Type": "application/json"},
                        success: function(data) {
                            if (data.status === "OK") {
                                $.messager.show({
                                    title: '{{ _("Success") }}',
                                    msg: data.message,
                                    timeout: 3000,
                                    showType: 'slide'
                                });
                                $("#user_html_table").datagrid('reload'); // Refresh the data grid
                            } else {
                                $.messager.alert('{{ _("Error") }}', data.message, 'error');
                            }
                        },
                        error: function() {
                            $.messager.alert('{{ _("Error") }}', '{{ _("An error occurred while trying to delete the USER.") }}', 'error');
                        }
                    });
                }
        });
        
    
    }
    

    

global_functions.userAddNewUser = function(row)   {
    
    global_functions.user_reset_form();
    
    $('#user_html_form_container')
    .dialog({
        title: '{{ _("New USER") }}',
        width: 500,
        height: 400,
        onClose: function() {
            //user_reset_form();
        },
        modal: true,
        onOpen: function() {
            var user_html_form_input_name = $('#user_html_form_input_name'),
            user_html_form_input_email = $('#user_html_form_input_email'),
            user_html_form_input_phone = $('#user_html_form_input_phone'),
            user_html_form_input_password = $('#user_html_form_input_password'),
            user_html_form_input_user_acgs_table = $('#user_html_form_input_user_acgs_table'),
            user_html_form_input_user_acg_0 = $('#user_html_form_input_user_acg_0'),
            user_html_form_user_acgs_add = $('#user_html_form_user_acgs_add'),
            user_html_form_user_acgs_remove =$('#user_html_form_user_acgs_remove');

            user_html_form_input_name.textbox({
                labelWidth: 100
            });
            user_html_form_input_email.textbox({
                validType: 'email',
                labelWidth: 100
            });
            user_html_form_input_phone.textbox({
                validType: 'number',
                labelWidth: 100
            });
            user_html_form_input_password.passwordbox({
                required: false,
                labelWidth: 150,
                prompt: 'Password',
                showEye: true
            });
            
            global_functions.user_make_acgs_combobox(user_html_form_input_user_acg_0);
            if (typeof row.id != 'undefined') {
                console.log(row);
                user_html_form_input_name.textbox('setValue',row.name);
                user_html_form_input_name.textbox('setText',row.name);

                user_html_form_input_email.textbox('setValue',row.email);
                user_html_form_input_email.textbox('setText',row.email);

                user_html_form_input_phone.textbox('setValue',row.phone);
                user_html_form_input_phone.textbox('setText',row.phone);
                global_functions.user_remove_all_user_acg();
                for (var i=0; i < row.user_acgs.length; i++) {
                    console.log(row.user_acgs[i]);
                    global_functions.user_add_user_acg(row.user_acgs[i]);
                }
            } else {
                global_functions.user_remove_all_user_acg();
                global_functions.user_add_user_acg({});
            }

            user_html_form_user_acgs_add.linkbutton({
                iconCls: 'icon-add',
                onClick: function () {
                    global_functions.user_add_user_acg({});
                }
            });
            user_html_form_user_acgs_remove.linkbutton({
                iconCls: 'icon-cancel',
                onClick: function() {
                    global_functions.user_remove_user_acg({});
                }
            })

        },
        buttons: [{
            text:'{{ _("Save") }}',
                handler:function(){
                    if (typeof row.id != 'undefined') {
                        global_functions.user_form_submit(row.id);   
                    } else {
                        global_functions.user_form_submit(0);
                    }
                }
            },{
            text:'Close',
                handler:function(){
                    $('#user_html_form_container').dialog('close');
                    global_functions.user_reset_form();
                }
            }],
    });

    //$('#user_html_form_id').form('clear');
}

global_functions.user_reset_form = function() {
    $('#user_html_form_input_user_acgs_table tr:last-child').remove(); 
    global_functions.user_add_user_acg({});
    $("#user_html_form_id").form('reset')
}

global_functions.user_make_acgs_combobox = function (element)
{
    element.combobox({
        url: '{{ url_for("acg.getAcgsForCombo") }}',
        method : 'get',
        valueField: 'id',
        textField: 'text',
        labelWidth: '120'
    });
}


global_functions.user_add_user_acg = function(rowData)
{
    var value = '';
    console.log(rowData);
    if (typeof rowData.acg_id != 'undefined') {
        value = rowData.acg_id;
    } 
    user_html_form_input_user_acgs_table = $('#user_html_form_input_user_acgs_table');
    var num = $('#user_html_form_input_user_acgs_table tr').length;
    var html_elem = '<input '
                    +'        id="user_html_form_input_user_acg_'+num+'" '
                    +'        name="user_acgs[]"   '
                    +'        class="easyui-combobox"   '
                    +'        value="'+value+'"         '
                    +'        required="true"           '
                    +'        label="{{ _('User ACG') }}" ' 
                    +'        style="width:100%" />   '
    var new_row = "<tr><td>"+html_elem+"</td><td></td></tr>";
    user_html_form_input_user_acgs_table.append(new_row);
    var element = $("#user_html_form_input_user_acg_"+num);
    global_functions.user_make_acgs_combobox(element);

}

global_functions.user_remove_user_acg = function()
{
    $('#user_html_form_input_user_acgs_table tr:last-child').remove(); 
}

global_functions.user_remove_all_user_acg = function()
{
    $('#user_html_form_input_user_acgs_table tr').remove(); 
}

global_functions.user_form_submit = function(id)
{
    if (!$("#user_html_form_id").form('validate')) {
        return;
    }
    $('#user_html_form_container').dialog('close');
    showProgress('{{ _('%(progression)s', progression=messages['progression']) }}', '{{ _('%(please_wait)s', please_wait=messages['please_wait']) }}');
    $("#user_html_form_id").form('submit', {
        url: id == 0 ? '{{ url_for("user.addUser") }}' : '{{ url_for("user.updateUser") }}',
        method: 'post',
        onSubmit: function(param){
            param.id = id;
        },
        success: function(data) {
            var res = JSON.parse(data);
            closeProgress();
            if (res.status != "OK"){
                $.messager.alert({
                    title: res.status,
                    msg: res.message,
                    fn: function(){
                        $('#user_html_form_container').dialog("open");
                    }
                });
            } else {
                $('#user_html_form_container').dialog("close");
                $.messager.show({
                    title: res.status,
                    msg:res.message,
                    timeout:3000,
                    showType:'slide'
                });
            }
            $("#user_html_table").datagrid("reload");
        }
    });
}

