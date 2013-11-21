// login 
function login(){
    var userName = $("#login_name").val();
    var userPassword = $("#login_password").val();
    $.ajax({
        type: 'post',
        url: "/api/user/current/",
        dataType: 'json',
        data: {
            user_name: userName,
            user_password: userPassword
        },
        async: false,
        success:function(data){
            if (data === null){
                alert('用户名或密码错误!');
                //location.href = '/';
            }else if(data.user_level == 'normal') {
                $("#user_info").empty();
                $('#login').modal('hide');
            }else if(data.user_level == 'uploader') {
                $("#user_info").empty();
                $('#login').modal('hide');
                $("#link_info").append('<li><a href="/admin/music/">Music</a></li>');
                $("#link_info").append('<li><a href="/admin/report/">Report</a></li>');
            }else if(data.user_level == 'admin') {
                $("#user_info").empty();
                $('#login').modal('hide');
                $("#link_info").append('<li><a href="/admin/music/">Music</a></li>');
                $("#link_info").append('<li><a href="/admin/report/">Report</a></li>');
                $("#link_info").append('<li><a href="/admin/user/">User</a></li>');
            }

            $("#user_info").append('<li><a><i class="icon-user"></i>&nbsp' + data.user_name+ '</a></li>');
            $("#user_info").append('<li><a id="user_listened">听过' + data.user_listened+ '首</a></li>');
            $("#user_info").append('<li><a id="user_favour">喜欢过' + data.user_favour.length + '首</a></li>');
            $("#user_info").append('<li><a id="logoutButton" href="#" onClick="logout()">注销</a></li>');

            $("#jp-report").html('<a href="#myModal" data-toggle="modal" data-toggle="tooltip" data-placement="top" title="举报" alt="report" onClick="reportError(this)"><img src="../static/img/report.png"></img></a>');
            $("#jp-favorite").html('<a href="#" data-toggle="tooltip" data-placement="top" title="喜欢" alt="favorite" onClick="favoriteSong(this)"><img src="../static/img/favorite2.png"></img></a>');
            $("#jp-trash").html('<a href="#" data-toggle="tooltip" data-placement="top" title="不喜欢" alt="trash" onClick="trashSong(this)"><img src="../static/img/trash2.png"></img></a>');
            songTag(data);
        }
    });
}

//register
function register(){
    var userName = $("#reg_name").val();
    var repeatPassword = $("#repeat_password").val();
    var userPassword = $("#reg_password").val();
    if (userPassword !== repeatPassword) {
        alert("密码输入不一致，请重新注册！");
    }else{
        $.ajax({
            type: 'post',
            url: "/api/user/",
            dataType: 'json',
            data: {
                user_name: userName,
                user_password: userPassword
            },
            async: false,
            success: function(data) {
                if (data == null){
                    alert('注册失败:用户名已存在!');
                }else{
                    alert('注册成功!');
                    //log in
                    $.ajax({
                        type: 'post',
                        url: "/api/user/current/",
                        dataType: 'json',
                        data: {
                            user_name: userName,
                            user_password: userPassword
                        },
                        async: false,
                        success:function(data){
                            $("#user_info").empty(); 
                            $('#register').modal('hide');                  
                            $("#user_info").append('<li><a><i class="icon-user"></i>&nbsp' + data.user_name+ '</a></li>');
                            $("#user_info").append('<li><a id="user_listened">听过' + data.user_listened+ '首</a></li>');
                            $("#user_info").append('<li><a id="user_favour">喜欢过' + data.user_favour.length + '首</a></li>');
                            $("#user_info").append('<li><a id="logoutButton" href="#" onClick="logout()">注销</a></li>');
                            //location.href = "/";
                            $("#jp-report").html('<a href="#myModal" data-toggle="modal" data-toggle="tooltip" data-placement="top" title="举报" alt="report" onClick="reportError(this)"><img src="../static/img/report.png"></img></a>');
                            $("#jp-favorite").html('<a href="#" data-toggle="tooltip" data-placement="top" title="喜欢" alt="favorite" onClick="favoriteSong(this)"><img src="../static/img/favorite2.png"></img></a>');
                            $("#jp-trash").html('<a href="#" data-toggle="tooltip" data-placement="top" title="不喜欢" alt="trash" onClick="trashSong(this)"><img src="../static/img/trash2.png"></img></a>');
                            songTag(data);
                        }
                    });
                }
            },
            error:function(){
                alert("注册失败，请重新输入！");
            }
        });
    } 
}

//logout
function logout() {
    $.ajax({
        type: 'delete',
        url: "/api/user/current/",
        async : false,
        success:function(data){
            location.href = '/';
        }
    });
}