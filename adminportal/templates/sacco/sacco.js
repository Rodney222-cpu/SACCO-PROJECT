

$("#sacco_html_table").datagrid({
    url: '{{ url_for("sacco.getSacco") }}',
    toolbar: '#sacco_html_table_toolbar',
    fit:true,
    pagination: true,
    rownumbers: true,
    columns: [[
        {field:'id', title:'ID',width:'5%'},
        {field:'group_id', title:'{{ _('GroupID') }}',width:'10%'},
        {field:'name', title:'{{ _('Name') }}',width:'20%'},
        {field:'location', title:'{{ _('Location') }}',width:'20%'},
        {field:'created_on', title:'{{ _('Created On') }}',width:'20%'},
        {field:'updated_on', title:'{{ _('Updated On') }}',width:'20%'},
        {field:'options', title:'{{ _('Options') }}', width:'15%',
            formatter: function(value,row,index) {
                console.log(row);
                return '<a href="#" class="label-anchor" onclick="global_functions.saccoLaunchUpdateDialog(\''+index+'\');">Edit</a> '
                    +' | '
                    +' <a href="#" class="label-anchor" onclick="global_functions.goToSaccoMembers(\''+index+'\', \''+row.sacco_name+'\');">Members ('+row.total_num_members+')</a> ';
            }
        }
    ]]
});

global_functions.saccoLaunchUpdateDialog = function(index) {
    var dataRows = $("#sacco_html_table").datagrid("getData");
    global_functions.saccoAddNewSacco(dataRows.rows[index]);
}


$("#sacco_html_table_toolbar_new_button").linkbutton({
    onClick: function () {
        global_functions.saccoAddNewSacco({});
    }
});

$("#sacco_html_table_toolbar_update_button").linkbutton({});


$("#sacco_html_table_toolbar_delete_button").linkbutton({
    onClick: function () {
        global_functions.saccoDeleteSacco({});
    }
});
    
global_functions.saccoDeleteSacco = function() {
        
    var rows = $("#sacco_html_table").datagrid('getSelections');
    if (rows.length < 1) {
        $.messager.alert('{{ _("Error") }}', '{{ _("Please select a SACCO to delete.") }}', 'error');
        return;
    }
    
    $.messager.confirm(
        '{{ _("Confirm") }}', '{{ _("Are you sure you want to delete this SACCO?") }}', 
        function(r){
            if (r){
                $.ajax({
                    url: '{{ url_for("sacco.deleteSacco") }}',
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
                            $("#sacco_html_table").datagrid('reload'); // Refresh the data grid
                        } else {
                            $.messager.alert('{{ _("Error") }}', data.message, 'error');
                        }
                    },
                    error: function() {
                        $.messager.alert('{{ _("Error") }}', '{{ _("An error occurred while trying to delete the SACCO.") }}', 'error');
                    }
                });
            }
    });
    

}


global_functions.goToSaccoMembers = function(index, saccoName) {
    var dataRows = $("#sacco_html_table").datagrid("getData");
    sacco = dataRows.rows[index];
    var encodedsaccoName = encodeURIComponent(saccoName);

    applayoutLoadRouteContent('{{ url_for("saccomember.index") }}?sacco_id='+sacco.id + '&sacco_name=' + encodedsaccoName,  'applayout_route_id_saccos');
}


global_functions.saccoAddNewSacco = function(row)   {
    
    global_functions.sacco_reset_form();

    $('#sacco_html_form_container')
    .dialog({
        title: '{{ _("New SACCO") }}',
        width: 500,
        height: 400,
        onClose: function() {
            //sacco_reset_form();
        },
        modal: true,
        onOpen: function() {
            var sacco_html_form_input_group_id = $('#sacco_html_form_input_group_id'),
            sacco_html_form_input_name = $('#sacco_html_form_input_name'),
            sacco_html_form_input_location = $('#sacco_html_form_input_location');


           

            sacco_html_form_input_group_id.textbox({
                validType: 'number',
                labelWidth: 125
            });
            sacco_html_form_input_name.textbox({
                validType: 'text',
                labelWidth: 125
            });
            sacco_html_form_input_location.textbox({
                validType: 'text',
                labelWidth: 125
            });

            if (typeof row.id != 'undefined') {
                console.log(row);
                sacco_html_form_input_group_id.textbox('setValue',row.group_id);
                sacco_html_form_input_group_id.textbox('setText',row.group_id);

                sacco_html_form_input_name.textbox('setValue',row.name);
                sacco_html_form_input_name.textbox('setText',row.name);

                sacco_html_form_input_location.textbox('setValue',row.location);
                sacco_html_form_input_location.textbox('setText',row.location);

            } else {
                
            }
   
        },
        buttons: [{
            text:'{{ _("Save") }}',
                handler:function(){
                    if (typeof row.id != 'undefined') {
                        global_functions.sacco_form_submit(row.id);   
                    } else {
                        global_functions.sacco_form_submit(0);
                    }
                }
            },{
            text:'Close',
                handler:function(){
                    $('#sacco_html_form_container').dialog('close');
                    global_functions.sacco_reset_form();
                }
            }],
    });

    //$('#sacco_html_form_id').form('clear');
}



global_functions.sacco_reset_form = function() {
    $("#sacco_html_form_id").form('reset')
}

global_functions.sacco_form_submit = function(id)
{
    if (!$("#sacco_html_form_id").form('validate')) {
        return;
    }
    $('#sacco_html_form_container').dialog('close');
    showProgress('{{ _('%(progression)s', progression=messages['progression']) }}', '{{ _('%(please_wait)s', please_wait=messages['please_wait']) }}');
    $("#sacco_html_form_id").form('submit', {
        url: id == 0 ? '{{ url_for("sacco.addSacco") }}' : '{{ url_for("sacco.updateSacco") }}',
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
                        $('#sacco_html_form_container').dialog("open");
                    }
                });
            } else {
                $('#sacco_html_form_container').dialog("close");
                $.messager.show({
                    title: res.status,
                    msg:res.message,
                    timeout:3000,
                    showType:'slide'
                });
            }
            $("#sacco_html_table").datagrid("reload");
        }
    });
}


