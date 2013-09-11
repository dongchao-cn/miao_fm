var myPlaylist = [];

/*Init Page*/
function InitPage()
{
    var req = '/api/music/next/';
    return HandleNext(req)
}

/*歌曲切换 Ajax请求*/
function HandleNext(req)
{
    var xmlhttp;
    // ajax to get data
    if (window.XMLHttpRequest)
    {// code for IE7+, Firefox, Chrome, Opera, Safari
            xmlhttp=new XMLHttpRequest();
    }
    else
    {// code for IE6, IE5
            xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    
    // console.info(req);
    
    xmlhttp.open("GET",req,false);

    xmlhttp.send();

    var json = '[' + xmlhttp.responseText + ']';
            
    var result = eval(json);
            
    return ProcessJson(result);
}


function ProcessJson(result)
{
    var myPlaylist = [];

    var re = result[0];
    
    var mp3_url = result[0]['music_url'];
    var mp3_title = result[0]['music_name'];
    var mp3_artist = result[0]['music_artist'];
    var mp3_rating = 5;
    var mp3_cover = '1.png';


    myPlaylist = [];

    var new_dic = {};
    new_dic['mp3'] = mp3_url;
    new_dic['title'] = mp3_title;
    new_dic['artist'] = mp3_artist;
    new_dic['rating'] = mp3_rating;
    //new_dic['cover'] = mp3_cover;

    myPlaylist.push(new_dic);
    // console.info(myPlaylist[0]['title'] + 'AJAX');
    return myPlaylist;
}