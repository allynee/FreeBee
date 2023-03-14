<template>

    <div>
        <h1></h1>
    </div>
</template>

<script>

import { geocode } from '../../../backend/simple_microservices/geocoding/geocoding.js'

export default {
    mounted:{
        geocoding(){
            geocode();
        }
    }
}
</script>