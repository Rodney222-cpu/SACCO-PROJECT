
$("#acgs_html_table").datagrid({
    url: '{{ url_for("acg.getAcgs") }}',
    toolbar: '#acgs_html_table_toolbar',
    fit:true,
    pagination: true,
    rownumbers: true,
    columns: [[
        {field:'id', title:'ID',width:'5%'},
        {field:'name', title:'{{ _('Name') }}',width:'18%'},
        {field:'created_on', title:'{{ _('Created On') }}',width:'30%'},
        {field:'updated_on', title:'{{ _('Updated On') }}',width:'30%'},
        {field:'options', title:'{{ _('Options') }}', width:'15%',
            formatter: function(value,row,index) {
                console.log(row);
                return '<a href="#" class="label-anchor" onclick="global_functions.acgLaunchUpdateDialog(\''+index+'\');">Edit</a>';
            }
        }
    ]]
});

global_functions.acgLaunchUpdateDialog = function(index) {
    var dataRows = $("#acgs_html_table").datagrid("getData");
    global_functions.acgsAddNewAcg(dataRows.rows[index]);
}

$("#acgs_html_table_toolbar_new_button").linkbutton({
    onClick: function () {
        global_functions.acgsAddNewAcg({});
    }
});

$("#acgs_html_table_toolbar_update_button").linkbutton();

$("#acgs_html_table_toolbar_delete_button").linkbutton(
    {
        onClick: function () {
            global_functions.acgsDeleteAcg({});
        }
    }
);


    global_functions.acgsDeleteAcg = function() {
        
        var rows = $("#acgs_html_table").datagrid('getSelections');
        if (rows.length < 1) {
            $.messager.alert('{{ _("Error") }}', '{{ _("Please select an ACG to delete.") }}', 'error');
            return;
        }
        
        $.messager.confirm(
            '{{ _("Confirm") }}', '{{ _("Are you sure you want to delete this ACG?") }}', 
            function(r){
                if (r){
                    $.ajax({
                        url: '{{ url_for("acg.deleteAcgs") }}',
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
                                $("#acgs_html_table").datagrid('reload'); // Refresh the data grid
                            } else {
                                $.messager.alert('{{ _("Error") }}', data.message, 'error');
                            }
                        },
                        error: function() {
                            $.messager.alert('{{ _("Error") }}', '{{ _("An error occurred while trying to delete the ACG.") }}', 'error');
                        }
                    });
                }
        });
        
    
    }
    

    

global_functions.acgsAddNewAcg = function(row)   {
    
    global_functions.acgs_reset_form();
    
    $('#acgs_html_form_container')
    .dialog({
        title: '{{ _("New ACG") }}',
        width: 500,
        height: 400,
        onClose: function() {
            //acgs_reset_form();
        },
        modal: true,
        onOpen: function() {
            var acgs_html_form_input_name = $('#acgs_html_form_input_name'),
            acgs_html_form_input_privileges_table = $('#acgs_html_form_input_privileges_table'),
            acgs_html_form_input_privilege_0 = $('#acgs_html_form_input_privilege_0');
            acgs_html_form_privileges_add = $('#acgs_html_form_privileges_add');
            acgs_html_form_privileges_remove =$('#acgs_html_form_privileges_remove')

            acgs_html_form_input_name.textbox();
            global_functions.acgs_make_privilegs_combobox(acgs_html_form_input_privilege_0);
            if (typeof row.id != 'undefined') {
                console.log(row);
                acgs_html_form_input_name.textbox('setValue',row.name);
                acgs_html_form_input_name.textbox('setText',row.name);
                global_functions.acgs_remove_all_privilege();
                for (var i=0; i < row.acg_privileges.length; i++) {
                    global_functions.acgs_add_privilege(row.acg_privileges[i]);
                }
            } else {
                global_functions.acgs_remove_all_privilege();
                global_functions.acgs_add_privilege({});
            }

            acgs_html_form_privileges_add.linkbutton({
                iconCls: 'icon-add',
                onClick: function () {
                    global_functions.acgs_add_privilege({});
                }
            });
            acgs_html_form_privileges_remove.linkbutton({
                iconCls: 'icon-cancel',
                onClick: function() {
                    global_functions.acgs_remove_privilege({});
                }
            })

        },
        buttons: [{
            text:'{{ _("Save") }}',
                handler:function(){
                    if (typeof row.id != 'undefined') {
                        global_functions.acgs_form_submit(row.id);   
                    } else {
                        global_functions.acgs_form_submit(0);
                    }
                }
            },{
            text:'Close',
                handler:function(){
                    $('#acgs_html_form_container').dialog('close');
                    global_functions.acgs_reset_form();
                }
            }],
    });

    //$('#acgs_html_form_id').form('clear');
}

global_functions.acgs_reset_form = function() {
    $('#acgs_html_form_input_privileges_table tr:last-child').remove(); 
    global_functions.acgs_add_privilege({});
    $("#acgs_html_form_id").form('reset')
}

global_functions.acgs_make_privilegs_combobox = function (element)
{
    element.combobox({
        url: '{{ url_for("acg.acgsGetPrivilegesForCombo") }}',
        valueField: 'id',
        textField: 'text',
        labelWidth: '120'
    });
}


global_functions.acgs_add_privilege = function(rowData)
{
    var value = '';
    console.log(rowData);
    if (typeof rowData.privilege_name != 'undefined') {
        value = rowData.privilege_name;
    } 
    acgs_html_form_input_privileges_table = $('#acgs_html_form_input_privileges_table');
    var num = $('#acgs_html_form_input_privileges_table tr').length;
    var html_elem = '<input '
                    +'        id="acgs_html_form_input_privilege_'+num+'" '
                    +'        name="privilage_name[]"   '
                    +'        class="easyui-combobox"   '
                    +'        value="'+value+'"         '
                    +'        required="true"           '
                    +'        label="{{ _('Privilege Name') }}" ' 
                    +'        style="width:100%" />   '
    var new_row = "<tr><td>"+html_elem+"</td><td></td></tr>";
    acgs_html_form_input_privileges_table.append(new_row);
    var element = $("#acgs_html_form_input_privilege_"+num);
    global_functions.acgs_make_privilegs_combobox(element);

}

global_functions.acgs_remove_privilege = function()
{
    $('#acgs_html_form_input_privileges_table tr:last-child').remove(); 
}

global_functions.acgs_remove_all_privilege = function()
{
    $('#acgs_html_form_input_privileges_table tr').remove(); 
}

global_functions.acgs_form_submit = function(id)
{
    if (!$("#acgs_html_form_id").form('validate')) {
        return;
    }
    $('#acgs_html_form_container').dialog('close');
    showProgress('{{ _('%(progression)s', progression=messages['progression']) }}', '{{ _('%(please_wait)s', please_wait=messages['please_wait']) }}');
    $("#acgs_html_form_id").form('submit', {
        url: id == 0 ? '{{ url_for("acg.addAcg") }}' : '{{ url_for("acg.updateAcg") }}',
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
                        $('#acgs_html_form_container').dialog("open");
                    }
                });
            } else {
                $.messager.show({
                    title: res.status,
                    msg:res.message,
                    timeout:3000,
                    showType:'slide'
                });
            }
            $("#acgs_html_table").datagrid("reload");
        }
    });
}