

$("#members_html_table").datagrid({
    url: '{{ url_for("members.getMember") }}?sacco_id={{ session["sacco"]["id"] }} ',
    toolbar: '#members_html_table_toolbar',
    fit:true,
    pagination: true,
    rownumbers: true,
    columns: [[
        {field:'id', title:'ID',width:'5%'},
        {field:'sacco_id', title:'{{ _('Sacco ID') }}',width:'10%'},
        {field:'fname', title:'{{ _('First Name') }}',width:'20%'},
        {field:'lname', title:'{{ _('Last Name') }}',width:'20%'},
        {field:'phone', title:'{{ _('Phone') }}',width:'20%'},
        {field:'email', title:'{{ _('Email') }}',width:'20%'},
        {field:'role', title:'{{ _('Role') }}',width:'20%'},
        {field:'balance', title:'{{ _('Balance') }}',width:'20%'},
        {field:'created_on', title:'{{ _('Created On') }}',width:'20%'},
        {field:'updated_on', title:'{{ _('Updated On') }}',width:'20%'},
        {field:'options', title:'{{ _('Options') }}', width:'15%',
            formatter: function(value,row,index) {
                console.log(row);
                return '<a href="#" class="label-anchor" onclick="global_functions.membersLaunchUpdateDialog(\''+index+'\');">Edit</a> '
                +'|'
                +'<a href="#" class="label-anchor" onclick="global_functions.goToTransactions(\''+index+'\', \''+row.fname+'\');">Transactions Profile</a> '
            }
        }
    ]]
});

global_functions.membersLaunchUpdateDialog = function(index) {
    var dataRows = $("#members_html_table").datagrid("getData");
    global_functions.membersAddNewMember(dataRows.rows[index]);
}


$("#members_html_table_toolbar_new_button").linkbutton({
    onClick: function () {
        global_functions.membersAddNewMember({});
    }
});

$("#members_html_table_toolbar_delete_button").linkbutton({
    onClick: function () {
        global_functions.membersDeleteMember({});
    }
});


global_functions.membersAddNewMember = function(row)   {

    global_functions.members_reset_form();

    $('#members_html_form_container')
    .dialog({
        title: '{{ _("NEW MEMBER") }}',
        width: 700,
        height: 400,
        onClose: function() {
            //members_reset_form();
        },
        modal: true,
        onOpen: function() {
            var members_html_form_input_account_number = $('#members_html_form_input_account_number'),
                members_html_form_input_fname = $('#members_html_form_input_fname'),
                members_html_form_input_lname = $('#members_html_form_input_lname'),
                members_html_form_input_gender = $('#members_html_form_input_gender'),
                members_html_form_input_phone = $('#members_html_form_input_phone'),
                members_html_form_input_email= $('#members_html_form_input_email'),
                members_html_form_input_role = $('#members_html_form_input_role'),
                members_html_form_input_next_of_kin_name = $('#members_html_form_input_next_of_kin_name'),
                members_html_form_input_date_of_birth = $('#members_html_form_input_date_of_birth');
                members_html_form_input_password = $('#members_html_form_input_password');

            members_html_form_input_account_number.textbox({
                validType: 'number',
                labelWidth: 200
            });
            members_html_form_input_fname.textbox({
                validType: 'text',
                labelWidth: 125
            });
            members_html_form_input_lname.textbox({
                validType: 'text',
                labelWidth: 125

            });
            members_html_form_input_gender.combobox({
                valueField:"label",
                textField: "value",
                data:[
                    {label:"Male","value":"Male"},
                    {label:"Female","value":"Female"},
                ],
                labelWidth: 125
            });
            members_html_form_input_phone.textbox({
                validType: ["mobile", 'regex["^[0-9]{10,12}$", "Phone number must be exactly 12 digits."]'],
                labelWidth: 125
            });
            members_html_form_input_email.textbox({
                validType: 'email',
                labelWidth: 125
            });
            members_html_form_input_role.combobox({
                valueField:"label",
                textField: "value",
                data:[
                    {label:"CHAIRPERSON","value":"CHAIRPERSON"},
                    {label:"TREASURER","value":"TREASURER"},
                    {label:"SECRETARY","value":"SECRETARY"},
                    {label:"REGULAR MEMBER","value":"REGULAR MEMBER"},
                ],
                labelWidth: 125,
                value:"REGULAR MEMBER"
            });
            members_html_form_input_next_of_kin_name.textbox({
                validType: 'text',
                labelWidth: 125
            });
            members_html_form_input_date_of_birth.datebox({
                validType: 'date',
                labelWidth: 125
            });
            members_html_form_input_password.passwordbox({
                required: false,
                labelWidth: 150,
                prompt: 'Password',
                showEye: true
            })

            if (typeof row.id != 'undefined') {
                console.log(row);
                members_html_form_input_account_number.textbox('setValue',row.account_number);
                members_html_form_input_account_number.textbox('setText',row.account_number);

                members_html_form_input_fname.textbox('setValue',row.fname);
                members_html_form_input_fname.textbox('setText',row.fname);

                members_html_form_input_lname.textbox('setValue',row.lname);
                members_html_form_input_lname.textbox('setText',row.lname);

                members_html_form_input_gender.combobox('setValue',row.gender);
                members_html_form_input_gender.combobox('setText',row.gender);

                members_html_form_input_phone.textbox('setValue',row.phone);
                members_html_form_input_phone.textbox('setText',row.phone);

                members_html_form_input_email.textbox('setValue',row.email);
                members_html_form_input_email.textbox('setText',row.email);

                members_html_form_input_role.combobox('setValue',row.role);
                members_html_form_input_role.combobox('setText',row.role);

                members_html_form_input_next_of_kin_name.textbox('setValue', row.next_of_kin_name);
                members_html_form_input_next_of_kin_name.textbox('setText', row.next_of_kin_name);

                members_html_form_input_date_of_birth.datebox('setValue', row.date_of_birth);
                members_html_form_input_date_of_birth.datebox('setText', row.date_of_birth);

            } else {
                //global_functions.members_remove_role();
                //global_functions.members_add_role();
            }


        },
        buttons: [
            {
                text:'{{ _("Save") }}',
                handler:function(){
                    if (typeof row.id != 'undefined') {
                        global_functions.members_form_submit(row.id);
                    } else {
                        global_functions.members_form_submit(0);
                    }
                }
            },
            {
                text:'Close',
                handler:function(){
                    $('#members_html_form_container').dialog('close');
                    global_functions.members_reset_form();
                }
            }
        ]
    });

    //$('#members_html_form_id').form('clear');
};

global_functions.members_remove_role = function()
{
    $('#members_html_form_input_role_table tr').remove();
}

global_functions.members_reset_form = function() {
    //$('#members_html_form_input_role:last-child').remove();
    $("#members_html_form_id").form('reset')
}

global_functions.members_form_submit = function(id)
{

    if (!$("#members_html_form_id").form('validate')) {
        return;
    }
    $('#members_html_form_container').dialog('close');
    showProgress('{{ _('%(progression)s', progression=messages['progression']) }}', '{{ _('%(please_wait)s', please_wait=messages['please_wait']) }}');
    $("#members_html_form_id").form('submit', {
        url: id == 0 ? '{{ url_for("members.addMember") }}' : '{{ url_for("members.updateMember")}}',
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
                        $('#members_html_form_container').dialog("open");
                    }
                });
            } else {
                $('#members_html_form_container').dialog("close");
                $.messager.show({
                    title: res.status,
                    msg:res.message,
                    timeout:3000,
                    showType:'slide'
                });
            }
            $("#members_html_table").datagrid("reload");
        }
    });
}

global_functions.membersDeleteMember = function() {

    var rows = $("#members_html_table").datagrid('getSelections');
    if (rows.length < 1) {
        $.messager.alert('{{ _("Error") }}', '{{ _("Please select a SACCO MEMBER to delete.") }}', 'error');
        return;
    }

    $.messager.confirm(
        '{{ _("Confirm") }}', '{{ _("Are you sure you want to delete this SACCO MEMBER?") }}',
        function(r){
            if (r){
                $.ajax({
                    url: '{{ url_for("members.deleteMembers") }}',
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
                            $("#members_html_table").datagrid('reload'); // Refresh the data grid
                        } else {
                            $.messager.alert('{{ _("Error") }}', data.message, 'error');
                        }
                    },
                    error: function() {
                        $.messager.alert('{{ _("Error") }}', '{{ _("An error occurred while trying to delete the SACCO MEMBER.") }}', 'error');
                    }
                });
            }
    });


}

global_functions.goToTransactions = function(index, fname) {
    var dataRows = $("#members_html_table").datagrid("getData");
    var saccomember = dataRows.rows[index];
    var encodedfirstName = encodeURIComponent(fname);
    var url = '{{ url_for("transactions.index") }}?member_id=' +saccomember.id + '&fname=' + encodedfirstName;
    
    applayoutLoadRouteContent(url, 'applayout_route_id_transactions');
}









