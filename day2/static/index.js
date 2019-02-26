let vm = new Vue({
        el:'#app',
        data:{
            date:'',
        },
        mounted:function () {
            this.get_index()
        },
    //本来打算用接口的方式去前端渲染数据，发现并没有tornado的直接前端数据渲染方便
        methods:{
            get_index:function () {
                axios.get('http://localhost:8000/poem',{
                    responseType:'json'
                }).then(response=>{
                    this.date = response.data
                    alert(JSON.stringify(this.date))
                }).catch(error=>{
                    console.log(error.data)
                })
            }
        }
    })