let vm = new Vue({
    el:'#app',
    delimiters:['[[',']]'],
    data:{
        //数据对象 // v-model // v-show // err_message
        username:'',
        password:'',
        password2:'',
        mobile:'',
        allow:'',

        error_name:false,
        error_password:false,
        error_mobile:false,
        error_allow:false,

        error_name_message:'',
        error_mobile_message:'',
    },
    methods:{//定义事件方法
        check_username(){
            let re = /^[a-zA-Z0-9_-]{5,20}$/;
            if(re.test(this.username)){
                //匹配成功，不展示错误提示信息
                this.error_name = false;
            }else{
                //匹配失败，展示错误提示信息
                this.error_name_message = '请输入5-20个字符的用户名';
                this.error_name = true;
            }
        },
        check_password(){
            let re = /^[0-9A-Za-z]{8,20}$/;
            if (re.test(this.password)) {
                this.error_password = false;
            } else {
                this.error_password = true;
            }
        },
        check_password2(){
            if (this.password != this.password2) {
                this.error_password2 = true;
            } else {
                this.error_password2 = false;
            }
        },
        check_mobile(){
            let re = /^1[3-9]\d{9}$/;
            if (re.test(this.mobile)) {
                this.error_mobile = false;
            } else {
                this.error_mobile_message = '您输入的手机号格式不正确';
                this.error_mobile = true;
            }
        },
        check_allow(){
            if (!this.allow) {
                this.error_allow = true;
            } else {
                this.error_allow = false;
            }
        },
        on_submit(){
            this.check_username();
            this.check_password();
            this.check_password2();
            this.check_mobile();
            this.check_allow();

            // 在校验之后，注册数据中，只要有错误，就禁用掉表单的提交事件
            if ( this.error_name == true || this.error_password == true ||
                 this.error_password2 == true || this.mobile == true || 
                 this.allow == true) 
           {
                // 禁用掉表单的提交事件
                window.event.returnValue = false;
            }
        },
    }
});

