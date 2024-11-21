$("#transactions_html_table").datagrid({
    url: '{{ url_for("transactions.getTransaction") }}',
    fit:true,
    pagination: true,
    rownumbers: true,
    columns: [[
        {field:'id', title:'ID',width:'5%'},
        {field:'sacco_id', title:'{{ _('Sacco ID') }}',width:'10%'},
        {field:'member_id', title:'{{ _('Member ID') }}',width:'11%'},
        {field:'amount', title:'{{ _('Amount') }}',width:'20%'},
        {field:'narrative', title:'{{ _('Narrative') }}',width:'20%'},
        {field:'reference', title:'{{ _('Reference') }}',width:'20%'},
        {field:'status', title:'{{ _('Status') }}',width:'20%'},
        {field:'transaction_type', title:'{{ _('Transaction Type') }}',width:'20%'},
        {field:'payment_method', title:'{{ _('Payment Method') }}',width:'20%'},
        {field:'trace', title:'{{ _('Trace') }}',width:'20%'},
        {field:'check_status_trace', title:'{{ _('Status Trace') }}',width:'20%'},
        {field:'balance_before', title:'{{ _('Balance Before') }}',width:'20%'},
        {field:'balance_after', title:'{{ _('Balance After') }}',width:'20%'},
        {field:'created_on', title:'{{ _('Created On') }}',width:'20%'},
        {field:'updated_on', title:'{{ _('Updated On') }}',width:'20%'},
        {field:'completion_date', title:'{{ _('Completion Date') }}',width:'20%'},
    ]]
});

