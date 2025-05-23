

$("#transactions_html_table").datagrid({
    url: '{{ url_for("transactions.getTransactions") }}?member_id={{saccomember["id"]}}',
    toolbar: '#transactions_html_table_toolbar',
    fit:true,
    pagination: true,
    rownumbers: true,
    columns: [[
        {field:'id', title:'ID',width:'5%'},
        {field:'completion_date', title:'{{ _('Completion Date') }}',width:'20%'},
        {field:'member_id', title:'{{ _('Member ID') }}',width:'11%'},
        {field:'amount', title:'{{ _('Amount') }}',width:'20%'},
        {field:'narrative', title:'{{ _('Narrative') }}',width:'20%'},
        {field:'status', title:'{{ _('Status') }}',width:'20%'},
        {field:'transaction_type', title:'{{ _('Transaction Type') }}',width:'20%'},
        {field:'payment_method', title:'{{ _('Payment Method') }}',width:'20%'},
        {field:'created_on', title:'{{ _('Created On') }}',width:'20%'},
        {field:'updated_on', title:'{{ _('Updated On') }}',width:'20%'},
        {field:'option', title:'{{ _('Options')}}', width:'15%',
            formatter: function(value, row, index) {
                console.log(row);
                return '<a href="#" class="label-anchor" onclick="global_functions.transactionsLaunchUpdateDialog(\''+index+'\');">Edit</a> ';
            }
        }
    
    ]]
});

global_functions.transactionsLaunchUpdateDialog = function(index) {
    var dataRows = $("#transactions_html_table").datagrid("getData");
    global_functions.transactionAddNewTransaction(dataRows.rows[index]);
}

$("#transactions_html_table_toolbar_new_button").linkbutton({
    onClick: function () {
        global_functions.transactionAddNewTransaction({});
    }
});

$("#transactions_html_table_toolbar_update_button").linkbutton({});


$("#transactions_html_table_toolbar_delete_button").linkbutton({
    onClick: function () {
       // global_functions.transactionTransaction({});
    }
});

global_functions.goBackToSaccoMember = function() {
    applayoutLoadRouteContent('{{ url_for('members.index')}}', 'applayout_route_id_members');
}



global_functions.transactionAddNewTransaction = function(row) {

    global_functions.transaction_reset_form();
       $('#transactions_html_form_container')
    .dialog({
        title: '{{ _("New TRANSACTION")}}',
        width:700,
        height:400,
        onClose: function(){},
        modal:true,
        onOpen: function() {
               var transactions_html_form_input_amount = $('#transactions_html_form_input_amount')
               transactions_html_form_input_transaction_type = $('#transactions_html_form_input_transaction_type')
               transactions_html_form_input_payment_method = $('#transactions_html_form_input_payment_method')
               transactions_html_form_input_narrative = $('#transactions_html_form_input_narrative')

            transactions_html_form_input_amount.textbox({
                validType: 'number',
                labelWidth: 200
            });
            transactions_html_form_input_transaction_type.combobox({
                valueField:"label",
                textField:"value",
                data:[
                    {label:"DEPOSIT","value":"DEPOSIT"},
                    {label:"WITHDRAW","value":"WITHDRAW"},
                    {label:"LOAN REPAYMENT","value":"LOAN REPAYMENT"},
                ],
                labelWidth:125
            });
            transactions_html_form_input_payment_method.combobox({
                valueField:"label",
                textField:"value",
                data:[
                    {label:"CASH","value":"CASH"},
                    {label:"BANK TRANSFER","value":"BANK TRANSFER"},
                    {label:"MOBILE MONEY","value":"MOBILE MONEY"},
                ],
                labelWidth:125
            });
            transactions_html_form_input_narrative.textbox({
                validType:'text',
                labelWidth:'120'
            });


            if (typeof row.id != 'undefined') {
                console.log(row);
                transactions_html_form_input_amount.textbox('setValue',row.amount);
                transactions_html_form_input_amount.textbox('setText',row.amount);

                transactions_html_form_input_gender.combobox('setValue',row.transaction_type);
                transactions_html_form_input_gender.combobox('setText',row.trnsaction_type);

                transactions_html_form_input_payment_mehtod.combobox('setValue',row.payment_method);
                transactions_html_form_input_payment_mehtod.combobox('setText',row.payment_method);

                transactions_html_form_input_narrative.textbox('setValue', row.narrative);
                transactions_html_form_input_narrative.textbox('setText', row.narrative);

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
                        global_functions.transaction_form_submit(row.id);
                    } else {
                        global_functions.transaction_form_submit(0);
                    }
                }
            },
            {
                text:'Close',
                handler:function(){
                    $('#transactions_html_form_container').dialog('close');
                    global_functions.transaction_reset_form();
                }
            }
        ]
    })
}

global_functions.transaction_reset_form = function() {
    //$('#sacco_member_html_form_input_role:last-child').remove();
    $("#transactions_html_form_id").form('reset')
}

global_functions.transaction_form_submit = function(id)
{
    if (!$("#transactions_html_form_id").form('validate')) {
        return;
    }
    $('#transactions_html_form_container').dialog('close');
    showProgress('{{ _('%(progression)s', progression=messages['progression']) }}', '{{ _('%(please_wait)s', please_wait=messages['please_wait']) }}');
    $("#transactions_html_form_id").form('submit', {
        url: id == 0 ? '{{ url_for("transactions.addTransaction") }}' : '#',
        method: 'post',
        onSubmit: function(param){
            console.log("Member ID:", saccomember['id']);
            param.id = id;
            param.member_id = saccomember['id'];
        },
        success: function(data) {
            var res = JSON.parse(data);
            closeProgress();
            if (res.status != "OK"){
                $.messager.alert({
                    title: res.status,
                    msg: res.message,
                    fn: function(){
                        $('#transactions_html_form_container').dialog("open");
                    }
                });
            } else {
                $('#transactions_html_form_container').dialog("close");
                $.messager.show({
                    title: res.status,
                    msg:res.message,
                    timeout:3000,
                    showType:'slide'
                });
            }
            $("#transactions_html_table").datagrid("reload");
        }
    });
}





