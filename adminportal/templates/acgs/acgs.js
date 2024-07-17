$("#acgs_html_table").grid({
    url: '{{ url_for("auth.index") }}',
    fit:true,
    pagination: true
});