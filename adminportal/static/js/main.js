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