
$("#acgs_html_table").datagrid({

    url: '{{ url_for("auth.index") }}',
    toolbar: '#acgs_html_table_toolbar',
    fit:true,
    pagination: true
});

$("#acgs_html_table_toolbar_new_button").linkbutton({
    onClick: function () {
        acgsAddNewAcg();
    }
});

$("#acgs_html_table_toolbar_update_button").linkbutton();
$("#acgs_html_table_toolbar_delete_button").linkbutton();


function acgsAddNewAcg()   {
    acgs_reset_form();
    
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

            acgs_html_form_input_name.textbox({});
            acgs_make_privilegs_combobox(acgs_html_form_input_privilege_0);

            acgs_html_form_privileges_add.linkbutton({
                iconCls: 'icon-add',
                onClick: function () {
                    acgs_add_privilege();
                }
            });
            acgs_html_form_privileges_remove.linkbutton({
                iconCls: 'icon-cancel',
                onClick: function() {
                    acgs_remove_privilege();
                }
            })

        },
        buttons: [{
            text:'{{ _("Save") }}',
                handler:function(){
                    acgs_form_submit();
                }
            },{
            text:'Close',
                handler:function(){
                    $('#acgs_html_form_container').dialog('close');
                    acgs_reset_form();
                }
            }],
    });

    $('#acgs_html_form_id').form('clear');
}

function acgs_reset_form()
{
    $('#acgs_html_form_input_privileges_table tr:last-child').remove(); 
    acgs_add_privilege();
    $("#acgs_html_form_id").form('reset')
}

function acgs_make_privilegs_combobox(element)
{
    element.combobox({
        url: '{{ url_for("acg.acgsGetPrivilegesForCombo") }}',
        valueField: 'id',
        textField: 'text',
        labelWidth: '120'
    });
}


function acgs_add_privilege()
{
    acgs_html_form_input_privileges_table = $('#acgs_html_form_input_privileges_table');
    var num = $('#acgs_html_form_input_privileges_table tr').length;
    var html_elem = '<input '
                    +'        id="acgs_html_form_input_privilege_'+num+'" '
                    +'        name="privilage_name[]"   '
                    +'        class="easyui-combobox"   '
                    +'        required="true"           '
                    +'        label="{{ _('Privilege Name') }}" ' 
                    +'        style="width:100%" />   '
    var new_row = "<tr><td>"+html_elem+"</td><td></td></tr>";
    acgs_html_form_input_privileges_table.append(new_row);
    var element = $("#acgs_html_form_input_privilege_"+num);
    acgs_make_privilegs_combobox(element);

}

function acgs_remove_privilege()
{
    $('#acgs_html_form_input_privileges_table tr:last-child').remove(); 
}

function acgs_form_submit()
{
    if (!$("#acgs_html_form_id").form('validate')) {
        return;
    }
    $('#acgs_html_form_container').dialog('close');
    showProgress('{{ _('%(progression)s', progression=messages['progression']) }}', '{{ _('%(please_wait)s', please_wait=messages['please_wait']) }}');
    $("#acgs_html_form_id").form('submit', {
        url: '{{ url_for("acg.addAcg") }}',
        method: 'post',
        success: function(data) {
            closeProgress();
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
                $('#acgs_html_form_container').dialog("open");
            }
        }
    });
}