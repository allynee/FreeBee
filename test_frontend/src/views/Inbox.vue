<template>
    <v-container class="py-10">  
        <v-row justify="center" class="text-center my-10" data-aos="fade-down">
            <v-col cols="2">
                <v-img :src="require('../assets/koala.png')" contain height="200"/>
            </v-col>
            <v-col cols="12">
                <h1 class="text-h4 brown--text text-center">Chat with Other Users</h1>
            </v-col>
            <v-col cols="8" align="center" >
                <p class="text-h6 font-weight-light brown--text text--darken-2">
                    Chat with other users who may potentially have found your lost pet or would like to find out more about the found pet you listed!
                </p>
            </v-col>
        </v-row>
        <v-divider></v-divider>
        <div 
        class="my-5"
        ref="talkjs"
        style="width:90%; margin=30px; height:500px;"
        id="talkjs-container">
            <i>Loading chat....</i>
        </div>
    </v-container>
</template>


<script>
    import Talk from "talkjs"

    export default{
        name:"Inbox",
        data(){
            return{
                // user:this.$store.getters.getuser,
                // conversation:null,
                chatbox:undefined,
                // index:1,

            }
        },
        // methods:{
        //     reRender(){
        //         this.index++
        //     }
        // },
        // props:{
        //     // currentUser:{
        //     //     type:Object,
        //     //     required:true,
        //     // }
        // },

        async mounted(){
            // localStorage.clear('https://app.talkjs.com')

            
            await Talk.ready
                console.log(this.user.userid)
                const me=new Talk.User({
                    id:this.user.userid,    
                    name: this.user.username,
                    email: this.user.email, 
                })

                //now hardcoding from firebase
                const others_obj=this.$store.getters.getOthers
                console.log(others_obj)

                const other=new Talk.User({
                    id:others_obj.userid,
                    name:others_obj.username,
                    email:others_obj.email,
                })
            
                // console.log(me)
                window.talkSession=new Talk.Session({
                appId:'tB4yzcUA',
                me:me,
            })

            const conversation= window.talkSession.getOrCreateConversation(
                Talk.oneOnOneId(me, other)
            )
            conversation.setParticipant(me)
            conversation.setParticipant(other)

            const inbox=window.talkSession.createInbox();
            inbox.select(conversation)
            inbox.mount(this.$refs.talkjs)



            

        },
        computed:{
            user(){
                return this.$store.getters.getuser
            }
        }

    }
</script>



