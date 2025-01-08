close_process = true;
/*
* Displays the process dialog.
* 
* @Param String title       -This is the title of the progress box.
* @Param String message     - This is the message to show in the progress title
*
* Returns void.
*/
function showProgress(title, message)
{
    close_process = false;
    var win = $.messager.progress({
        title: title,
        msg:message,
        onBeforeClose: function () {
            if (close_process)
                return true;
            else
                return false;
        }
    });
}

/*
* closesProcess closes progress bar.
* 
* 
*/
function closeProgress()
{
    close_process=true;
    $.messager.progress('close');
}



var global_functions = {
    acgLaunchUpdateDialog: function (){},
    acgs_add_privilege: function(){}
};

 
$.fn.datebox.defaults.formatter = function(date) {
    var y = date.getFullYear();
    var m = date.getMonth()+1;
    var m_string = m < 10 ? "0"+m : m;
    var d = date.getDate();
    var d_string = d < 10 ? "0"+d : d;
    return y+'-'+m_string+'-'+d_string;
}

$.fn.datebox.defaults.parser = function(s){
    if (!s) {
        return new Date();
    }

    var ss = s.split('-');
    var d = parseInt(ss[2],10);
    var m = parseInt(ss[1],10);
    var y = parseInt(ss[0],10);
	var t = Date.parse(s);
	if (!isNaN(y) && !isNaN(m) && !isNaN(d)){
		return new Date(y,m-1, d);
	} else {
		return new Date();
	}
}