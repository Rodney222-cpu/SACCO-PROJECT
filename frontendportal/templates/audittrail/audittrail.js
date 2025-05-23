$("#audit_trail_html_table").datagrid({
    url: '{{ url_for("audittrail.getAuditTrail") }}',
    fit:true,
    pagination: true,
    rownumbers: true,
    columns: [[
        {field:'id', title:'ID',width:'5%'},
        {field:'user_name', title:'{{ _('Username') }}',width:'10%'},
        {field:'email', title:'{{ _('Email') }}',width:'20%'},
        {field:'action', title:'{{ _('Action') }}',width:'20%'},
        {field:'data', title:'{{ _('Data') }}',width:'20%'},
        {field:'created_on', title:'{{ _('Created On') }}',width:'20%'},
        {field:'updated_on', title:'{{ _('Updated On') }}',width:'20%'},
    ]]
});
