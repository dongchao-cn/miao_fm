/* storage the current song info */
var currentSongInfo = [];
var favoLabel;
var trashLabel;
var title;

$(document).ready(function(){
    //title = $("title").text();
    //console.info('music_#####ist 1' + currentSongInfo);

    //jplayer init
    new jPlayerPlaylist({
        jPlayer: "#jquery_jplayer_1",
        cssSelectorAncestor: "#jp_container_1"
    }, 
    [],
    { 
        ready: playReady,
        ended: playEnded,
        swfPath: "/static/jPlayer/js",
        supplied: "mp3",
        wmode: "window",
        smoothPlayBar: true,
        keyEnabled: true
    });


    $("#jp-next").click(function() {
        playNextSong("next");
    });

    $("#jp-report").html('<a href="#" data-toggle="tooltip" data-placement="top" title="请注册后使用!" alt="report" ><img src="../static/img/report.png"></img></a>');
    $("#jp-favorite").html('<a href="#" data-toggle="tooltip" data-placement="top" title="请注册后使用!" alt="favorite" o><img src="../static/img/favorite2.png"></img></a>');
    $("#jp-trash").html('<a href="#" data-toggle="tooltip" data-placement="top" title="请注册后使用!" alt="trash" ><img src="../static/img/trash2.png"></img></a>');  

    //side bar init
    $("#extruderRight").buildMbExtruder({
        position: "right",
        width: 350,
        extruderOpacity: .8,
        textOrientation: "tb",
        onExtOpen: function() {},
        onExtContentLoad: function() {},
        onExtClose: function() {}
    });

    $.fn.changeLabel = function(text) {
        $(this).find(".flapLabel").html(text);
        $(this).find(".flapLabel").mbFlipText();
    };

    //vote bar initial
    $("#container div a").click(function() {
        $(this).parent().animate({
            width: '+=1px'
        }, 500);
        $(this).prev().html(parseInt($(this).prev().html()) + 1);
        return false;
    });
});

/*
*   Jplayer funcitons
*/

function playReady() {
    favoLabel = 1;
    trashLabel = 1;
    $.ajax({
        type: "get",
        url: "/api/music/next/",
        dataType: "json",
        cache: false,
        async: false,
        success:function(data) {
            //console.info(data);
            var singer = data.music_artist;
            var name = data.music_name;
            var album = data.music_album;
            currentSongInfo = [data.music_id, data.music_name, data.music_artist, data.music_album];
            //console.info('music_#####ist 2    ' + currentSongInfo);
            //$("title").text(title + " - " + name);
            $("#jp-singer").text(singer); 
            marqueeShow(name, album);

            if(data.music_img == '') {
                $('#jp-cover').empty();
                $('#jp-cover').append('<img src="/static/img/default.jpg" />');
            }else {
                $('#jp-cover').empty();
                $('#jp-cover').append('<img src="' + data.music_img + '" />');
            }

            //send two get http request?
            //console.info('music_#####ist 3    ' + currentSongInfo);
            player = $("#jquery_jplayer_1");
            player.jPlayer("setMedia", {
                mp3: data.music_url
            });
            player.jPlayer("load");
            player.jPlayer("play");


            str_listened = $("#user_listened").text();
            int_listened = parseInt(str_listened.substring(2, str_listened.length - 1));
            // console.info(int_listened)
            int_listened += 1;
            $("#user_listened").text("听过" + int_listened + "首");  
        },
        error: function() {
            // console.info('load music failed!!');
        }
    });

    $.ajax({
        type: 'get',
        url: "/api/user/current/",
        async : false,
        dataType: "json",
        success:function(data){
            //console.info(data);
            if (data !== null){
                $("#jp-report").html('<a href="#myModal" data-toggle="modal" data-toggle="tooltip" data-placement="top" title="举报" alt="report" onClick="reportError(this)"><img src="../static/img/report.png"></img></a>');
                $("#jp-favorite").html('<a href="#" data-toggle="tooltip" data-placement="top" title="喜欢" alt="favorite" onClick="favoriteSong(this)"><img src="../static/img/favorite2.png"></img></a>');
                $("#jp-trash").html('<a href="#" data-toggle="tooltip" data-placement="top" title="不喜欢" alt="trash" onClick="trashSong(this)"><img src="../static/img/trash2.png"></img></a>');
                songTag(data);
            }
        }   
    });
}

function playEnded() {
    favoLabel = 1;
    trashLabel = 1;
    $.ajax({
        type: "get",
        url: "/api/music/next/",
        dataType: "json",
        cache: false,
        async: false,
        success:function(data) {
            //console.info(data);
            //console.info('load ended music ok');
            var singer = data.music_artist;
            var name = data.music_name;
            var album = data.music_album;
            currentSongInfo = [data.music_id, data.music_name, data.music_artist, data.music_album];

            $("#jp-singer").text(singer); 
            marqueeShow(name, album);

            if(data.music_img == '') {
                $('#jp-cover').empty();
                $('#jp-cover').html('<img src="/static/img/default.jpg" />');
            }else {
                $('#jp-cover').empty();
                $('#jp-cover').html('<img src="' + data.music_img + '" />');
            }

            //send two get http request?
            player = $("#jquery_jplayer_1");
            player.jPlayer( "clearMedia" );
            player.jPlayer("setMedia", {
                mp3: data.music_url
            });
            player.jPlayer("play");

            str_listened = $("#user_listened").text();
            int_listened = parseInt(str_listened.substring(2, str_listened.length - 1));
            // console.info(int_listened)
            int_listened += 1;
            $("#user_listened").text("听过" + int_listened + "首");  
        },
        error: function() {
            // console.info('load music failed!!');
        }
    });

    $.ajax({
        type: 'get',
        url: "/api/user/current/",
        async : false,
        dataType: "json",
        success:function(data){
            //console.info(data);
            //console.info('load user ok');
            if (data !== null){
                $("#jp-report").html('<a href="#myModal" data-toggle="modal" data-toggle="tooltip" data-placement="top" title="举报" alt="report" onClick="reportError(this)"><img src="../static/img/report.png"></img></a>');
                $("#jp-favorite").html('<a href="#" data-toggle="tooltip" data-placement="top" title="喜欢" alt="favorite" onClick="favoriteSong(this)"><img src="../static/img/favorite2.png"></img></a>');
                $("#jp-trash").html('<a href="#" data-toggle="tooltip" data-placement="top" title="不喜欢" alt="trash" onClick="trashSong(this)"><img src="../static/img/trash2.png"></img></a>');
                songTag(data);
            }
        }   
    });
}
function playNextSong(musicStr) {
    favoLabel = 1;
    trashLabel = 1;
    $.ajax({
        type: "get",
        url: "/api/music/" + musicStr + "/",
        dataType: "json",
        cache: false,
        async: false,
        success:function(data) {
            //console.info(data);
            //console.info('load music ok');
            var singer = data.music_artist;
            var name = data.music_name;
            var album = data.music_album;
            currentSongInfo = [data.music_id, data.music_name, data.music_artist, data.music_album];

            $("#jp-singer").text(singer); 
            marqueeShow(name, album);

            if(data.music_img == '') {
                $('#jp-cover').empty();
                $('#jp-cover').html('<img src="/static/img/default.jpg" />');
            }else {
                $('#jp-cover').empty();
                $('#jp-cover').html('<img src="' + data.music_img + '" />');
            }

            //send two get http request?
            $("#jquery_jplayer_1").jPlayer("setMedia", {
                mp3: data.music_url
            }).jPlayer("play");

            str_listened = $("#user_listened").text();
            int_listened = parseInt(str_listened.substring(2, str_listened.length - 1));
            int_listened += 1;
            $("#user_listened").text("听过" + int_listened + "首");  
        },
        error: function() {
             console.info('load music failed!!');
        }
    });

    $.ajax({
        type: 'get',
        url: "/api/user/current/",
        async : false,
        dataType: "json",
        success:function(data) {
            //console.info(data);
            //console.info('load user ok');
            if (data !== null){
                $("#jp-report").html('<a href="#myModal" data-toggle="modal" data-toggle="tooltip" data-placement="top" title="举报" alt="report" onClick="reportError(this)"><img src="../static/img/report.png"></img></a>');
                $("#jp-favorite").html('<a href="#" data-toggle="tooltip" data-placement="top" title="喜欢" alt="favorite" onClick="favoriteSong(this)"><img src="../static/img/favorite2.png"></img></a>');
                $("#jp-trash").html('<a href="#" data-toggle="tooltip" data-placement="top" title="不喜欢" alt="trash" onClick="trashSong(this)"><img src="../static/img/trash2.png"></img></a>');
                songTag(data);
            }
        }   
    });
}

function reportError() {
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
function submitReport() {
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
        success:function() {
            // console.info("success");
        },
        error:function() {
             console.info("error");
        }
    });
}

//favorite button 
function favoriteSong() {
    //console.info(favoLabel);
    if(favoLabel == 1 && trashLabel == 1) {  
        favoLabel = 0;  
        postFavSong();   
    } else if(favoLabel == 1 && trashLabel == 0) {
        favoLabel = 0;
        trashLabel = 1;
        postFavSong();
        delTrashSong();       
    } else {
        favoLabel = 1;
        delFavSong();    
    }   
}

//trash button 
function trashSong() {
    //console.info(trashLabel);
    if(trashLabel == 1 && favoLabel == 1) {
        trashLabel = 0;
        postTrashSong();   
    }else if(trashLabel == 1 && favoLabel == 0) {
        trashLabel = 0;
        favoLabel = 1;
        postTrashSong();
        delFavSong();
        
    }else{  
        trashLabel = 1;      
        delTrashSong();
    }   
}

//song taged favour or dislike
function songTag(data) {
    //console.info(data);
    // console.info("currentSongInfo" + currentSongInfo[0]);
    // console.info("data.user_favour" + data.user_favour);

    for(var i = 0; i < data.user_favour.length; i += 1) {
        if(currentSongInfo[0] === data.user_favour[i]) {
            // console.info("favorite");
            $("#jp-favorite img").attr("src", "/static/img/favorite.png");
            favoLabel = 0;
            break;
        } else {
            //console.info("no fav");
            favoLabel = 1;
            $("#jp-favorite img").attr("src", "/static/img/favorite2.png");
        }
        
    }

    //console.info('trash list');
    for(var i = 0; i < data.user_dislike.length; i += 1) {
        if(currentSongInfo[0] === data.user_dislike[i]) {
            // console.info("dislike");
            $("#jp-trash img").attr("src", "/static/img/trash.png");
            trashLabel = 0;
            break;
        } else {
            //console.info("no trash");
            trashLabel = 1;
            $("#jp-trash img").attr("src", "/static/img/trash2.png");
        }
        
    }
}


function postFavSong() {
    $.ajax({
        type: "post",
        url: "/api/user/current/favour/",
        async: true,
        dataType: "json",
        data: {
            music_id:currentSongInfo[0]
        },
        success:function() {
            $("#jp-favorite img").attr("src","../static/img/favorite.png");
            str_favour = $("#user_favour").text();
            int_favour = parseInt(str_favour.substring(3, str_favour.length - 1))
            // console.info(int_listened)
            int_favour += 1
            $("#user_favour").text("喜欢过"+int_favour+"首"); 
            // console.info("post fav success");
        },
        error:function() {
            // console.info("error");
        }
    });
}

function postTrashSong() {
     $.ajax({
        type: "post",
        url: "/api/user/current/dislike/",
        async: true,
        dataType: "json",
        data: {
            music_id:currentSongInfo[0]
        },
        success:function() {
            $("#jp-trash img").attr("src","../static/img/trash.png");
            // console.info("post dislike success");
        },
        error:function() {
            // console.info("error");
        }
    });
}

function delFavSong() {
    $.ajax({
        type: "delete",
        url: "/api/user/current/favour/" + currentSongInfo[0] + "/",
        async: true,
        dataType: "json",
        success: function() {
            $("#jp-favorite img").attr("src","../static/img/favorite2.png");
            str_favour = $("#user_favour").text();
            int_favour = parseInt(str_favour.substring(3, str_favour.length - 1));
            // console.info(int_listened)
            int_favour -= 1;
            $("#user_favour").text("喜欢过"+int_favour+"首"); 
            // console.info("delete fav success");
        },
        error: function() {
            // console.info("error");
        }
    });
}

function delTrashSong() {
    $.ajax({
        type: "delete",
        url: "/api/user/current/dislike/" + currentSongInfo[0] + "/",
        async: true,
        dataType: "json",
        success: function() {
            // console.info("delete dislike success");
            $("#jp-trash img").attr("src","../static/img/trash2.png");
        },
        error:function() {
            // console.info("error");
        }
    });
}


/*
*   marqueen show
*/
function characterCount(str) {

    var totalCount = 0;
    for(var i = 0; i < str.length; i += 1) {
        var c = str.charCodeAt(i); 
        if((c >= 0x0001 && c <= 0x007e) || (0xff60<=c && c<=0xff9f)) {  
           totalCount++;  
        }else {     
            totalCount += 2;  
        }  
    }
    return totalCount;
} 

function marqueeShow(name, album) {
    var lengthOfStr = characterCount(name + album);
    //console.info(lengthOfStr);
    if(lengthOfStr > 48) {
        $("#jp-nameAlbum").empty();
        $("#jp-nameAlbum").append('<marquee scrollamount="2"  behavior="scroll" hspace="6" onMouseOut="this.start()" \
                    onMouseOver="this.stop()"><span id="jp-name"></span><span id="jp-album"></span></marquee> ');
        $("#jp-name").text(name);  
        $("#jp-album").text(album);
    } 
    else {
        $("#jp-nameAlbum").empty();
        $("#jp-nameAlbum").append('<span id="jp-name"></span><span id="jp-album"></span>');
        $("#jp-name").text(name);  
        $("#jp-album").text(album);
    }
}