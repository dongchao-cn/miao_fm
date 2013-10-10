
function render_report_list(data){
    $("#addReport > tbody").empty();
    //console.info(data);
    for(var i = 0;i < data.length;++i){
        var tdstr = '<tr class="' + data[i].report_id + '"><td>'+data[i].report_id+'</td> \
            <td>'+data[i].report_music.music_id+'</td> \
            <td>' + data[i].report_info+'</td> \
            <td>'+ data[i].report_date +'</td> \
            <td><a href="#myModal3" class="btn  btn-success btn-xs" data-toggle="modal" onClick ="editReport(this)">Edit</a>&nbsp\
            <button id="' + data[i].report_id + '"class="btn btn-danger btn-xs" onClick ="delReport(this)">Ignore</button></td> \
            </tr>';
        //console.info(tdstr);
        $("#addReport > tbody:last").append(tdstr);
    }
}
function delReport(event){
    var reportId = event.id;
    url = '/api/report/' + reportId + '/';
    console.info(reportId);
    $.ajax({
        type:'delete',
        url:url,
        async : false,
        success:function(data){
            //console.info("delete" + data + "success!");
            $('.' + reportId).remove();
        },
    });

}

//delete Edit report
function delEditReport(evnet){
    delEditSong();
    //location.href = "/admin/report/";
    
}

//edit report 
function editReport(event){
    //console.info($(event).next().attr("id"));
    // console.info($(event).next().attr('id'))
    // console.info($('.'+$(event).next().attr('id'))[0].cells[1].innerText);
    var musicId = $('.'+$(event).next().attr('id'))[0].cells[1].innerText;
    //console.info("editreport");
    //console.info(musicId);

    $.ajax({
        type:'get',
        url: "/api/music/" + musicId + '/',
        async : false,
        dataType:'json',
        success:edit_music_success_modal,
        error:edit_music_error_modal
    });
}
