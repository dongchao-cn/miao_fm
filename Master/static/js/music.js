
function edit_music_success_modal(data){   
    //console.info(data);
    $("#editSong").empty();
    var strInputText =
    '<table> \
        <tr><td><span class="input-group-addon">music_id</span></td><td><input disabled="disabled" type="text" class="form-control" value="' + data.music_id +'"></td></tr>\
        <tr><td><span class="input-group-addon">music_name</span></td><td><input type="text" class="form-control"  value="' + data.music_name +'"></td></tr>\
        <tr><td><span class="input-group-addon">music_artist</span></td><td><input type="text" class="form-control"  value="' + data.music_artist +'"></td></tr>\
        <tr><td><span class="input-group-addon">music_album</span></td><td><input type="text" class="form-control"  value="' + data.music_album +'"></td></tr>\
        <tr><td><span class="input-group-addon">music_img</span></td><td><img src="' + data.music_img +'"></td></tr>\
        </table>\
        <audio controls ="controls" preload="none" src="' + data.music_url +'"/></audio></br>';
        
    $("#editSong").append(strInputText);
}

function edit_music_error_modal(data){
    $("#editSong").empty();
    var strInputText = '<p>Sorry,the song you find does not exist!</p>';
    $("#editSong").append(strInputText);
}

function render_music_list(data){
    $("#addSong > tbody").empty();
    // console.info(data);
    for(var i = 0;i < data.length;++i){
        var tdstr = '<tr class="' + data[i].music_id + '"><td>'+data[i].music_id+'</td> \
            <td>'+data[i].music_name+'</td> \
            <td>' + data[i].music_artist+'</td> \
            <td>'+ data[i].music_album +'</td> \
            <td><a href="#myModal3" class="btn btn btn-success btn-xs" data-toggle="modal" onClick ="editSong(this)">Edit</a>&nbsp\
            <button id="' + data[i].music_id + '"class="btn btn btn-danger btn-xs" onClick ="delSong(this)">Del</button></td> \
            </tr>';
        //console.info(tdstr);
        $("#addSong > tbody:last").append(tdstr);
    }
}

//delete song in edit box
function delEditSong(){
    //console.info($("#editSong table input").val());
    var musicId = $("#editSong table input").val();
    url = '/api/music/' + musicId + '/';
    $.ajax({
        type:'delete',
        url:url,
        async : false,
        success:function(data){
            //console.info("delete" + data + "success!");
            $('.' + musicId).remove();
        },
    });
    
}



