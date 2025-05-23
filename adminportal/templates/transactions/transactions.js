$("#transactions_html_table").datagrid({
    url: '{{ url_for("transactions.getTransaction") }}',
    fit:true,
    pagination: true,
    rownumbers: true,
    columns: [[
        {field:'id', title:'ID',width:'5%'},
        {field:'completion_date', title:'{{ _('Completion Date') }}',width:'20%'},
        {field:'member_id', title:'{{ _('Member ID') }}',width:'11%'},
        {field:'amount', title:'{{ _('Amount') }}',width:'20%'},
        {field:'narrative', title:'{{ _('Narrative') }}',width:'20%'},
        {field:'reference', title:'{{ _('Reference') }}',width:'20%'},
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


