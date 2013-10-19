/* storage the current song info */
var currentSongInfo = [];

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

});

function playNextSong(){
    $.ajax({
        type:"get",
        url:"/api/music/next/",
        dataType:"json",
        cache:false,
        async:false,
        success:function(data){
            //console.info(data);
            var singer = data.music_artist;
            var name = data.music_name;
            var album = data.music_album;
            currentSongInfo = [data.music_id,data.music_name,data.music_artist,data.music_album];
            $("#jp-singer").text(singer); 
            $("#jp-name").text(name);  
            $("#jp-album").text(album); 
            $("#jquery_jplayer_1").jPlayer("setMedia", {
                mp3:data.music_url
            });
            $("#jquery_jplayer_1").jPlayer("play");
            str_listened = $("#user_listened").text();
            int_listened = parseInt(str_listened.substring(2, str_listened.length-1))
            // console.info(int_listened)
            int_listened += 1
            $("#user_listened").text("听过"+int_listened+"首");
        }
    });
}

function reportError(){
    //console.info(currentSongInfo[1]);
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

function submitReport(){
    var reportContent = $("#reportContent").val();
    //console.info(reportContent);
    $.ajax({
        type:"post",
        url:"/api/report/",
        async:false,
        dataType:"json",
        data:{
            music_id:currentSongInfo[0],
            report_info:reportContent
        },
        success:function(){
            //console.info("success");
        },
        error:function(){
            //console.info("error");
        }
    });
}