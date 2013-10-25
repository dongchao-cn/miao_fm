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
                location.href = '/';
            }else{
               location.href = '/';
            }
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
                    location.href = '/';
                }
            },
            error:function(){
                alert("注册失败，请重新输入！");
            }
        });
    } 
}