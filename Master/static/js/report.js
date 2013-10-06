
function render_report_list(data)
{
    $("#addReport > tbody").empty();
    // console.info(data);
    for(var i = 0;i < data.length;++i){
        var tdstr = '<tr class="' + data[i].report_id + '"><td>'+data[i].report_id+'</td> \
            <td>'+data[i].report_music.music_id+'</td> \
            <td>' + data[i].report_info+'</td> \
            <td>'+ data[i].report_date +'</td> \
            <td><a href="#myModal3" class="btn btn btn-success btn-xs" data-toggle="modal" onClick ="editSong(this)">edit</a>&nbsp\
            <button id="' + data[i].report_id + '"class="btn btn btn-danger btn-xs" onClick ="delReport(this)">del</button></td> \
            </tr>';
        //console.info(tdstr);
        $("#addReport > tbody:last").append(tdstr);
    }
}