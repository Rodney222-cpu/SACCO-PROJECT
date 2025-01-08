

$("#members_html_table").datagrid({
    //url: '{{ url_for("saccomember.getSaccoMember") }}',
    toolbar: '#members_html_table_toolbar',
    fit:true,
    pagination: true,
    rownumbers: true,
    columns: [[
        {field:'id', title:'ID',width:'5%'},
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
                return '<a href="#" class="label-anchor" onclick="global_functions.membersLaunchUpdateDialog(\''+index+'\');">Edit</a> ';
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

$("#sacco_member_html_table_toolbar_update_button").linkbutton({});


    
//global_functions.saccomemberAddNewSaccoMember = function(row)   {
    
    global_functions.sacco_member_reset_form();
    
    $('#sacco_member_html_form_container')
    .dialog({
        title: '{{ _("New SACCO MEMBER") }}',
        width: 700,
        height: 400,
        onClose: function() {
            //sacco_member_reset_form();
        },
        modal: true,
        onOpen: function() {
            var sacco_member_html_form_input_account_number = $('#sacco_member_html_form_input_account_number'),
                sacco_member_html_form_input_fname = $('#sacco_member_html_form_input_fname'),
                sacco_member_html_form_input_lname = $('#sacco_member_html_form_input_lname'),
                sacco_member_html_form_input_gender = $('#sacco_member_html_form_input_gender'),
                sacco_member_html_form_input_phone = $('#sacco_member_html_form_input_phone'),
                sacco_member_html_form_input_email= $('#sacco_member_html_form_input_email'),
                sacco_member_html_form_input_role = $('#sacco_member_html_form_input_role'),
                sacco_member_html_form_input_balance = $('#sacco_member_html_form_input_balance'),
                sacco_member_html_form_input_next_of_kin_name = $('#sacco_member_html_form_input_next_of_kin_name'),
                sacco_member_html_form_input_date_of_birth = $('#sacco_member_html_form_input_date_of_birth');

            sacco_member_html_form_input_account_number.textbox({
                validType: 'number',
                labelWidth: 200
            });
            sacco_member_html_form_input_fname.textbox({
                validType: 'text',
                labelWidth: 125
            });
            sacco_member_html_form_input_lname.textbox({
                validType: 'text',
                labelWidth: 125
                
            });
            sacco_member_html_form_input_gender.combobox({
                valueField:"label",
                textField: "value",
                data:[
                    {label:"Male","value":"Male"},
                    {label:"Female","value":"Female"},
                ],
                labelWidth: 125
            });
            sacco_member_html_form_input_phone.textbox({
                validType: 'mobile',
                labelWidth: 125
            });
            sacco_member_html_form_input_email.textbox({
                validType: 'email',
                labelWidth: 125
            });
            sacco_member_html_form_input_role.combobox({
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
            sacco_member_html_form_input_balance.textbox({
                validType: 'text',
                labelWidth: 125
            });
            sacco_member_html_form_input_next_of_kin_name.textbox({
                validType: 'text',
                labelWidth: 125
            });
            sacco_member_html_form_input_date_of_birth.datebox({
                validType: 'date',
                labelWidth: 125
            });

            if (typeof row.id != 'undefined') {
                console.log(row);
                sacco_member_html_form_input_account_number.textbox('setValue',row.account_number);
                sacco_member_html_form_input_account_number.textbox('setText',row.account_number);

                sacco_member_html_form_input_fname.textbox('setValue',row.fname);
                sacco_member_html_form_input_fname.textbox('setText',row.fname);

                sacco_member_html_form_input_lname.textbox('setValue',row.lname);
                sacco_member_html_form_input_lname.textbox('setText',row.lname);

                sacco_member_html_form_input_gender.combobox('setValue',row.gender);
                sacco_member_html_form_input_gender.combobox('setText',row.gender);

                sacco_member_html_form_input_phone.textbox('setValue',row.phone);
                sacco_member_html_form_input_phone.textbox('setText',row.phone);

                sacco_member_html_form_input_email.textbox('setValue',row.email);
                sacco_member_html_form_input_email.textbox('setText',row.email);

                sacco_member_html_form_input_role.combobox('setValue',row.role);
                sacco_member_html_form_input_role.combobox('setText',row.role);

                sacco_member_html_form_input_balance.textbox('setValue', row.balance);
                sacco_member_html_form_input_balance.textbox('setText', row.balance);

                sacco_member_html_form_input_next_of_kin_name.textbox('setValue', row.next_of_kin_name);
                sacco_member_html_form_input_next_of_kin_name.textbox('setText', row.next_of_kin_name);

                sacco_member_html_form_input_date_of_birth.datebox('setValue', row.date_of_birth);
                sacco_member_html_form_input_date_of_birth.datebox('setText', row.date_of_birth);

            } else {
                //global_functions.sacco_member_remove_role();
                //global_functions.sacco_member_add_role();   
            }

   
        },
        buttons: [
            {
                text:'{{ _("Save") }}',
                handler:function(){
                    if (typeof row.id != 'undefined') {
                        global_functions.sacco_member_form_submit(row.id);   
                    } else {
                        global_functions.sacco_member_form_submit(0);
                    }
                }
            },
            {
                text:'Close',
                handler:function(){
                    $('#sacco_member_html_form_container').dialog('close');
                    global_functions.sacco_member_reset_form();
                }
            }
        ]
    });

    //$('#sacco_member_html_form_id').form('clear');
}

global_functions.sacco_member_remove_role = function()
{
    $('#sacco_member_html_form_input_role_table tr').remove(); 
}


global_functions.sacco_member_reset_form = function() {
    //$('#sacco_member_html_form_input_role:last-child').remove(); 
    $("#sacco_member_html_form_id").form('reset')
}


global_functions.sacco_member_form_submit = function(id)
{

    if (!$("#sacco_member_html_form_id").form('validate')) {
        return;
    }
    $('#sacco_member_html_form_container').dialog('close');
    showProgress('{{ _('%(progression)s', progression=messages['progression']) }}', '{{ _('%(please_wait)s', please_wait=messages['please_wait']) }}');
    $("#sacco_member_html_form_id").form('submit', {
        url: id == 0 ? '{{ url_for("saccomember.addSaccoMember") }}' : '{{ url_for("saccomember.updateSaccoMember")}}',
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
                        $('#sacco_member_html_form_container').dialog("open");
                    }
                });
            } else {
                $('#sacco_member_html_form_container').dialog("close");
                $.messager.show({
                    title: res.status,
                    msg:res.message,
                    timeout:3000,
                    showType:'slide'
                });
            }
            $("#sacco_member_html_table").datagrid("reload");
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    
    //Function to get a URL parameter value by its name
    function getUrlParameter(name) {
        const urlParams  = new URLSearchParams(window.location.search);
        return urlParams.get(name);
    }

    //retrieve the SACCO name from the URL
    const saccoName = getUrlParameter('sacco_name');

    if (saccoName) {
        const saccoNameElement = document.getElementById('sacco_member_html_table_sacco_name');
        saccoNameElement.textContent = 'SACCO: ' + decodeURIComponent(saccoName);
    }
});

