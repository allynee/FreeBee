<template>
<v-container>
    <v-toolbar flat>
        <v-text-field outlined prepend-icon="mdi-magnify" 
            class="rounded-xl px-5"
            label="Search for a FreeBee" clearable v-model="search" @change="emitValue()">
        </v-text-field>
    </v-toolbar>
</v-container>
</template>

<script>
export default{
    data(){
        return{
            search:''
        }
    },
    methods:{
        emitValue(){
            this.$emit("search", this.search)
        }
    }
}
// return 
</script>