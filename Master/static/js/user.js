
function edit_user_success_modal(data)
{
    console.info(data)
    $("#editUser").empty();
    var strInputText =
    '<table> \
        <tr><td><span class="input-group-addon">user_id</span></td><td><input disabled="disabled" type="text" class="form-control" value="' + data.user_id +'"></td></tr>\
        <tr><td><span class="input-group-addon">user_name</span></td><td><input disabled="disabled" type="text" class="form-control"  value="' + data.user_name +'"></td></tr>\
        <tr><td><span class="input-group-addon">user_password</span></td><td><input disabled="disabled" type="text" class="form-control"  value="' + data.user_password +'"></td></tr>\
        <tr><td><span class="input-group-addon">user_level</span></td><td>\
        <select class="form-control">\
        <option value="normal">normal</option>\
        <option value="uploader">uploader</option>\
        <option value="admin">admin</option>\
        </select></td></tr>\
        </table>';
    $("#editUser").append(strInputText);
}

function edit_user_error_modal(data)
{
    $("#editUser").empty();
    var strInputText = '<p>Sorry,the song you find does not exist!</p>';
    $("#editUser").append(strInputText);
}


function render_report_list(data)
{
    $("#addUser > tbody").empty();
    // console.info(data);
    for(var i = 0;i < data.length;++i){
        var tdstr = '<tr class="' + data[i].user_id + '"><td>'+data[i].user_id+'</td> \
            <td>'+data[i].user_name+'</td> \
            <td>' + data[i].user_password+'</td> \
            <td>'+ data[i].user_level +'</td> \
            <td><a href="#myModal3" class="btn btn btn-success btn-xs" data-toggle="modal" onClick ="editUser(this)">Edit</a>&nbsp\
            <button id="' + data[i].user_id + '"class="btn btn btn-danger btn-xs" onClick ="delUser(this)">Del</button></td> \
            </tr>';
        //console.info(tdstr);
        $("#addUser > tbody:last").append(tdstr);
    }
}