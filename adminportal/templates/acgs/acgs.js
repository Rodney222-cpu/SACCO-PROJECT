
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
    $('#acgs_html_form_container')
    .dialog({
        title: '{{ _("New ACG") }}',
        width: 500,
        height: 400,
        onClose: function() {
            dialog_elem.panel('destroy');
        },
        modal: true,
        buttons: [{
            text:{{ _("Save") }}'',
                handler:function(){
                    var validate = $("#"+dialogs.form_id).form('validate');
                    if (validate) {
                        $("#"+dialogs.form_id).form('submit', {
                            url: dialogs.submission_on_edit_url,
                            onSubmit: function() {
                                //$("#"+form_box_id).hide();
                                dialog_elem.panel("minimize");
                                showProgress(dialogs.form_submission);
                            },
                            success: function(data) {
                                closeProgress();
                                try {
                                    var json_req = jQuery.parseJSON(data);
                                } catch (ex) {
                                    displayE(dialogs.error_title,  ex+" "+ex.stack, "error", form_box_id);
                                }
                                if (json_req.error) {
                                    if (json_req.code == 10000) {
                                        showFormDialog(form_box_id);
                                        return displayExeptions(json_req.error, dialogs.error_title);
                                    }
                                    displayE(dialogs.error_title, json_req.error, "error", form_box_id);
                                } else {
                                    $("#"+form_box_id).dialog("close");
                                    $.messager.alert(json_req.dialog_title,
                                    json_req.data,
                                    "info",
                                    function(){
                                        $("#"+form_box_id).dialog("close");
                                        $("#"+dialogs.grid_id).datagrid('reload');
                                    });
                                }
                            },
                        });
                    }
                }
            },{
            text:'Close',
                handler:function(){
                    dialog_elem.panel('destroy');
                }
            }],
    });

    $('#acgs_html_form_id').form('clear');
}