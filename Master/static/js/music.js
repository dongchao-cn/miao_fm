//clear uploaded song list
$('#shutdown').bind('click',function(event){
    $('#clearlist').nextAll().remove();
});

//refresh song list
$('#refreshList').bind('click',function(event){
    //location.reload();
    $.ajax({
            type: 'get',
            url: "/api/music/",
            dataType:'json',
            data: {
                 start:0,
                 count:items_pre_page
            },
            async : true,
            success:function(data){
                $("#addSong > tbody").empty();
                console.info(data);
                for(var i = 0;i < data.length;++i){
                    var tdstr = 
                        '<tr class="' + data[i].music_id + '"><td>'+data[i].music_id+'</td> \
                        <td>'+ data[i].music_album +'</td> \
                        <td>' + data[i].music_artist+'</td> \
                        <td>'+data[i].music_name+'</td> \
                        <td><audio controls ="controls" preload="none" src="' + data[i].music_url +'"/><audio/></td>\
                        <td><a href="#myModal3" class="btn btn btn-success btn-xs" data-toggle="modal" onClick ="editSong(this)">edit</a>&nbsp\
                        <button id="' + data[i].music_id + '"class="btn btn btn-danger btn-xs" onClick ="delSong(this)">del</button></td> \
                        </tr>';
                        //console.info(tdstr);
                     $("#addSong > tbody:last").append(tdstr);
                    }              
                }
            });
});

//delete all the song list 
$('#deleteListAll').bind('click',function(event){
    $.ajax({
        type: 'delete',
        url: "/api/music/",
        async : false,
        success:function(){
            $("#addSong > tbody").empty(); 
         }
        });
    });

//delete song 
function delSong(event){
    //console.info(event.id);
    var musicId = event.id;
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

//edit song 
function editSong(event){
    //console.info($(event).next().attr('id'));
    var musicId = $(event).next().attr('id');
        $.ajax({
        type:'get',
        url: "/api/music/" + musicId + '/',
        async : false,
        success:function(data){
            var dataObj = eval('(' + data + ')');
            var musicId = dataObj.music_id;
            var musicAlbum = dataObj.music_album;
            var musicArtist = dataObj.music_artist;
            var musicName = dataObj.music_name;
            console.info(dataObj.music_url);
            console.info(dataObj);
            $("#editSong").empty();
                var strInputText = 
                      '<div class="input-group"><span class="input-group-addon">歌曲ID</span>\
                      &nbsp\
                      <input type="text" class="form-control" disabled="disabled" value="' + dataObj.music_id +'"></br>\
                      <span class="input-group-addon">专辑</span>&nbsp&nbsp&nbsp&nbsp&nbsp\
                      <input  type="text" class="form-control" value="' + dataObj.music_album +'"></br>\
                      <span class="input-group-addon">艺术家</span>\
                      &nbsp\
                      <input  type="text" class="form-control" value="' + dataObj.music_artist +'"></br>\
                      <span class="input-group-addon">歌曲</span>&nbsp&nbsp&nbsp&nbsp&nbsp\
                      <input  type="text" class="form-control" value="' + dataObj.music_name +'"></br>\
                      <audio controls ="controls" preload="none" src="' + dataObj.music_url +'"/><audio/>\
                    </div>';
                $("#editSong").append(strInputText);
        },
        
    });
    
}

//update song info
$('#updateSongInfo').bind('click',function(event){
    //$('#clearlist').nextAll().remove();
    var info = $('#editSong div').children();
    // console.info("##########");
    // console.info(info);
    // console.info($(info[1]).val());
    // console.info($(info[4]).val());
    // console.info($(info[7]).val());
    // console.info($(info[10]).val());

    var musicId = $(info[1]).val();
    var musicAlbum = $(info[4]).val();
    var musicArtist = $(info[7]).val();
    var musicName = $(info[10]).val();
    var url = "http://cdn.search-ebooks.org/music_file/" +  + '/';
    
    $.ajax({
        type:'put',
        url: '/api/music/' + musicId + '/',
        data:{
            music_album: musicAlbum,
            music_artist: musicArtist,
            music_name: musicName,
        },
        async : false,
        success:function(){
           //parent.location.reload();
           console.info($(this));
           var tdstr = '<tr class="' + musicId + '"><td>'+ 歌曲Id +'</td> \
                            <td>'+ 专辑 +'</td> \
                            <td>' + 音乐家 +'</td> \
                            <td>'+ 歌曲 +'</td> \
                            <td><a href="#myModal3" class="btn btn btn-success btn-xs" data-toggle="modal" onClick ="editSong(this)">编辑</a>&nbsp \
                            <button id="' + musicId + '"class="btn btn btn-danger btn-xs" onClick ="delSong(this)">删除</button></td> \
                            </tr>';
           $('.' + musicId).replaceWith(tdstr);

         }
     });
    
});
    
//search song info
function searchMusic(){
    var musicId = $('#searchMusicId').val();
    console.info(musicId);
    $.ajax({
        type:'get',
        url: "/api/music/" + musicId + '/',
        async : false,
        success:function(data){
            var dataObj = eval('(' + data + ')');
            var musicId = dataObj.music_id;
            var musicAlbum = dataObj.music_album;
            var musicArtist = dataObj.music_artist;
            var musicName = dataObj.music_name;
            console.info(dataObj.music_url);
            console.info(dataObj);
            $("#editSong").empty();
                var strInputText = 
                      '<div class="input-group"><span class="input-group-addon">歌曲ID</span>&nbsp\
                      <input type="text" class="form-control" disabled="disabled" value="' + dataObj.music_id +'"></br>\
                      <span class="input-group-addon">专辑</span>&nbsp&nbsp&nbsp&nbsp\
                      <input  type="text" class="form-control" value="' + dataObj.music_album +'"></br>\
                      <span class="input-group-addon">艺术家</span>&nbsp\
                      <input  type="text" class="form-control" value="' + dataObj.music_artist +'"></br>\
                      <span class="input-group-addon">歌曲</span>&nbsp&nbsp&nbsp&nbsp\
                      <input  type="text" class="form-control" value="' + dataObj.music_name +'"></br>\
                      <audio controls ="controls" preload="none" src="' + dataObj.music_url +'"/><audio/>\
                    </div>';
                $("#editSong").append(strInputText);
        },
        error:function(){
            $("#editSong").empty();
            var strInputText = '<p>你搜索的歌曲不存在！</p>';
            $("#editSong").append(strInputText);
        }
    });

}

$('#myModal3').on('hidden', function () {
    $("#editSong").empty();
})

$('#myModal').on('hidden', function () {
    location.reload();
})

//上传文件
$(function(){
    $('#fileupload').fileupload({
        dataType: 'json',
        add: function (e, data) { 
            console.info(data.files[0].name);           
            $('<h6/>').text(data.files[0].name).appendTo($('#upload'));           
            console.info(data);
            data.context = $('<button type="button" class="btn btn-mini btn-info"/>').text('开始上传')
                .appendTo($('#upload'))
                .click(function () {
                    data.context = $('<button type="button" class="btn btn-mini btn-info"/>').text('上传中......').replaceAll($(this));
                    data.submit();
                });
        },
        done: function (e, data) {
            data.context.text('上传完成!');
            console.info(data.files[0]);
            $.ajax({
            type: 'get',
            url: "/api/music/",
            dataType:'json',
            data: {
                 start:0,
                 count:items_pre_page
            },
            async : true,
            success:function(data){
                $("#addSong > tbody").empty();
                // for(var i = 0;i < data.length;++i){
                //     var tdstr = '<tr class="' + data[i].music_id + '"><td>'+data[i].music_id+'</td> \
                //     <td>'+ data[i].music_album +'</td> \
                //     <td>' + data[i].music_artist+'</td> \
                //     <td>'+data[i].music_name+'</td> \
                //     <td><a href="#myModal3" class="btn btn btn-success btn-xs" data-toggle="modal" onClick ="editSong(this)">edit</a>&nbsp\
                //     <button id="' + data[i].music_id + '"class="btn btn btn-danger btn-xs" onClick ="delSong(this)">del</button></td> \
                //         </tr>';
                //         //console.info(tdstr);
                //      $("#addSong > tbody:last").append(tdstr);
                    // }              
                }
            });

        }
    });

    
});

items_pre_page = 10

$.ajax( {
    url:'/api/music/',// 跳转到 action
    type:'get',
    dataType:'json',
    success:function(data) {
        var options = {
            currentPage: 1,
            totalPages: Math.floor(data.total_count / items_pre_page) + 1,
            onPageClicked: function(e,originalEvent,type,page){
                $.ajax({
                    type: 'get',
                    url: "/api/music/",
                    dataType:'json',
                    data: {
                        start:(page-1)*items_pre_page,
                        count:items_pre_page
                    },
                    async : false,
                    success:function(data){
                        console.info(data.length);
                        $("#addSong > tbody").empty();
                        for(var i = 0;i < data.length;++i){
                            var tdstr = '<tr class="' + data[i].music_id + '"><td>'+data[i].music_id+'</td> \
                            <td>'+ data[i].music_album +'</td> \
                            <td>' + data[i].music_artist+'</td> \
                            <td>'+data[i].music_name+'</td> \
                            <td><a href="#myModal3" class="btn btn btn-success btn-xs" data-toggle="modal" onClick ="editSong(this)">edit</a>&nbsp \
                            <button id="' + data[i].music_id + '"class="btn btn btn-danger btn-xs" onClick ="delSong(this)">del</button></td> \
                            </tr>';
                            //console.info(tdstr);
                            $("#addSong > tbody:last").append(tdstr);
                        }                  
                    }
                });
            }
        }
        $('.paginator').bootstrapPaginator(options);
     },
     error : function() {
          alert("异常！");
     }
 });


$(document).ready(function(){
    $.ajax({
        type: 'get',
        url: "/api/music/",
        dataType:'json',
        data: {
            start:0,
            count:items_pre_page
        },
        async : false,
        success:function(data){
            $("#addSong > tbody").empty();
            console.info(data);
            for(var i = 0;i < data.length;++i){
                var tdstr = '<tr class="' + data[i].music_id + '"><td>'+data[i].music_id+'</td> \
                <td>'+ data[i].music_album +'</td> \
                <td>' + data[i].music_artist+'</td> \
                <td>'+data[i].music_name+'</td> \
                <td><a href="#myModal3" class="btn btn btn-success btn-xs" data-toggle="modal" onClick ="editSong(this)">编辑</a>&nbsp\
                <button id="' + data[i].music_id + '"class="btn btn btn-danger btn-xs" onClick ="delSong(this)">删除</button></td> \
                </tr>';
                //console.info(tdstr);
                $("#addSong > tbody:last").append(tdstr);
            }                  
        }
    });
});
