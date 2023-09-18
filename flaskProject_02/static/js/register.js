
function bindEmailCaptchaClick(){
    $("#captcha-btn").click(function (event){
        var $this = $(this);
        // 阻止默认事件
        event.preventDefault();

        var email = $("input[name='email']").val();
        $.ajax({
            url: "/customer/captcha/email?email="+email,
            method: "GET",
            success: function (result){
                var code = result['code']
                if(code == 200){
                    var countdown = 5;
                    $this.off("click");
                    var timer = setInterval(function (){
                        $this.text(countdown);
                        countdown -= 1;
                        if(countdown <= 0){
                            // 清掉定时器
                            clearInterval(timer);
                            $this.text("获取验证码");
                        //     重新绑定点击事件
                            bindEmailCaptchaClick();
                        }
                    }, 1000);
                    // alert("验证码发送成功")
                }else {
                    alert(result['message'])
                }
            },
            fail: function (error){
                console.log(error);
            }
        })

    });
}
// 写在这个函数里面的是等整个网页加载完毕后才执行
$(function (){

    bindEmailCaptchaClick();

});