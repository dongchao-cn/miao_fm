/* storage the current song info */
var currentSongInfo = [];
var favoLabel = 1;
var trashLabel = 1;

$(document).ready(function(){
    new jPlayerPlaylist({
        jPlayer: "#jquery_jplayer_1",
        cssSelectorAncestor: "#jp_container_1"
    }, 
    [],{ 
        ready: playNextSong,
        ended: playNextSong,
        swfPath: "/static/jPlayer/js",
        supplied: "mp3",
        wmode: "window",
        smoothPlayBar: true,
        keyEnabled: true
    });

    $("#jp-next").click(function(){
        //console.info("click next");
        playNextSong();
    });

    $("#jp-report").html('<a href="#" data-toggle="modal tooltip" data-placement="top" title="请注册后使用!" alt="report" ><img src="../static/img/report.png"></img></a>');
    $("#jp-favorite").html('<a href="#" data-toggle="modal tooltip" data-placement="top" title="请注册后使用!" alt="favorite" o><img src="../static/img/favorite2.png"></img></a>');
    $("#jp-trash").html('<a href="#" data-toggle="modal tooltip" data-placement="top" title="请注册后使用!" alt="trash" ><img src="../static/img/trash2.png"></img></a>');

    $.ajax({
        type: 'get',
        url: "/api/user/current/",
        async : true,
        dataType: "json",
        success:function(data){
            if (data !== null){
                // $("#jp-report").html('<a href="#myModal" data-toggle="modal tooltip" data-placement="top" title="举报" alt="report" onClick="reportError(this)"><img src="../static/img/report.png"></img></a>');
                $("#jp-report").html('<a href="#myModal" data-toggle="modal" data-toggle="tooltip" data-placement="top" title="举报" alt="report" onClick="reportError(this)"><img src="../static/img/report.png"></img></a>');
                $("#jp-favorite").html('<a href="#"  data-toggle="tooltip" data-placement="top" title="喜欢" alt="favorite" onClick="favoriteSong(this)"><img src="../static/img/favorite2.png"></img></a>');
                $("#jp-trash").html('<a href="#"  data-toggle="tooltip" data-placement="top" title="不喜欢" alt="trash" onClick="trashSong(this)"><img src="../static/img/trash2.png"></img></a>');
            }
        }   
    });   
});

function playNextSong(){
    $.ajax({
        type:"get",
        url:"/api/music/next/",
        dataType:"json",
        cache:false,
        async:false,
        success:function(data){
            console.info(data);
            var singer = data.music_artist;
            var name = data.music_name;
            var album = data.music_album;
            currentSongInfo = [data.music_id,data.music_name,data.music_artist,data.music_album];
            //console.info(currentSongInfo);
            $("#jp-singer").text(singer); 
            $("#jp-name").text(name);  
            $("#jp-album").text(album); 

            if(data.music_img == '') {
                $('#jp-cover').empty();
            }else {
                $('#jp-cover').html('<img src=' + data.music_img + '>');
            }

            $("#jquery_jplayer_1").jPlayer("setMedia", {
                mp3:data.music_url
            });
            $("#jquery_jplayer_1").jPlayer("play");
            str_listened = $("#user_listened").text();
            int_listened = parseInt(str_listened.substring(2, str_listened.length-1))
            // console.info(int_listened)
            int_listened += 1
            $("#user_listened").text("听过"+int_listened+"首");

            $.ajax({
                type: 'get',
                url: "/api/user/current/",
                async : true,
                dataType: "json",
                success:function(data){
                    if (data !== null){
                         songTag();
                    }
                }   
            });   
        }
    });
}

function reportError(){
    console.info(currentSongInfo[1]);
    $("#reportInfo").empty();
     var strInputText = 
        '<table> \
            <tr><td><span class="input-group-addon">歌曲ID</span></td><td><input type="text" class="form-control" disabled="disabled" value="' + currentSongInfo[0] +'"></td></tr>\
            <tr><td><span class="input-group-addon">歌名</span></td><td><input type="text" class="form-control" disabled="disabled" value="' + currentSongInfo[1] +'"></td></tr>\
            <tr><td><span class="input-group-addon">歌手</span></td><td><input type="text" class="form-control" disabled="disabled" value="' + currentSongInfo[2] +'"></td></tr>\
            <tr><td><span class="input-group-addon">专辑</span></td><td><input type="text" class="form-control" disabled="disabled" value="' + currentSongInfo[3] +'"></td></tr>\
            <tr><td><span class="input-group-addon">错误信息</span></td><td> <textarea id="reportContent" placeholder="请输入错误信息" type="textarea" class="form-control" value="" rows="3" cols="80"></textarea></td></tr>\
        </table>';
    $("#reportInfo").append(strInputText);    
}

//report button 
function submitReport(){
    var reportContent = $("#reportContent").val();
    //console.info(reportContent);
    $.ajax({
        type:"post",
        url:"/api/report/",
        async:true,
        dataType:"json",
        data:{
            music_id:currentSongInfo[0],
            report_info:reportContent
        },
        success:function(){
            console.info("success");
        },
        error:function(){
            console.info("error");
        }
    });
}

//favorite button 
function favoriteSong(){
    //console.info(favoLabel);
    if(favoLabel == 1 && trashLabel == 1){    
        postFavSong();
        favoLabel = 0;
    }else if(favoLabel == 1 && trashLabel == 0){
        postFavSong();
        favoLabel = 0;
        delTrashSong();
        trashLabel = 1;
    }else{
        delFavSong();
        favoLabel = 1;
    }   
}

//trash button 
function trashSong(){
    //console.info(trashLabel);
    if(trashLabel == 1 && favoLabel == 1){
        postTrashSong();
        trashLabel = 0;
    }else if(trashLabel == 1 && favoLabel == 0){
        postTrashSong();
        trashLabel = 0;
        delFavSong();
        favoLabel = 1;
    }else{        
        delTrashSong();
        trashLabel = 1;
    }   
}

//song taged favour or dislike
function songTag(){
    $.ajax({
        type:"get",
        url:"/api/user/current/",
        async:true,
        dataType:"json",
        success:function(data){
            //console.info(currentSongInfo);
            //console.info(data);
            for(var i = 0; i < data.user_favour.length;i += 1){
                if(currentSongInfo[0] == data.user_favour[i]){
                    // console.info("favorite");
                    $("#jp-favorite img").attr("src","../static/img/favorite.png");
                    favoLabel = 0;
                    break;
                }
                favoLabel = 1;
                $("#jp-favorite img").attr("src","../static/img/favorite2.png");
            }

            for(var i = 0; i < data.user_dislike.length;i += 1){
                if(currentSongInfo[0] == data.user_dislike[i]){
                    // console.info("dislike");
                    $("#jp-trash img").attr("src","../static/img/trash.png");
                    trashLabel = 0;
                    break;
                }
                trashLabel = 1;
                $("#jp-trash img").attr("src","../static/img/trash2.png");
            }
        }
    });
}

function postFavSong(){
    $.ajax({
        type:"post",
        url:"/api/user/current/favour/",
        async:true,
        dataType:"json",
        data:{
            music_id:currentSongInfo[0]
        },
        success:function(){
            $("#jp-favorite img").attr("src","../static/img/favorite.png");
            console.info("post fav success");
        },
        error:function(){
            console.info("error");
        }
    });
}

function postTrashSong(){
     $.ajax({
        type:"post",
        url:"/api/user/current/dislike/",
        async:true,
        dataType:"json",
        data:{
            music_id:currentSongInfo[0]
        },
        success:function(){
            $("#jp-trash img").attr("src","../static/img/trash.png");
            console.info("post dislike success");
        },
        error:function(){
            console.info("error");
        }
    });
}

function delFavSong(){
    $.ajax({
        type:"delete",
        url:"/api/user/current/favour/" + currentSongInfo[0] + "/",
        async:true,
        dataType:"json",
        success:function(){
            $("#jp-favorite img").attr("src","../static/img/favorite2.png");
            console.info("delete fav success");
        },
        error:function(){
            console.info("error");
        }
    });
}

function delTrashSong(){
    $.ajax({
        type:"delete",
        url:"/api/user/current/dislike/" + currentSongInfo[0] + "/",
        async:false,
        dataType:"json",
        success:function(){
            console.info("delete dislike success");
            $("#jp-trash img").attr("src","../static/img/trash2.png");
        },
        error:function(){
            console.info("error");
        }
    });
}