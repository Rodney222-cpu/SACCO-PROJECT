
$("#acgs_html_table").datagrid({
    url: '{{ url_for("auth.index") }}',
    fit:true,
    pagination: true
});
