import {store} from '../store/index.js'
export default(to,from,next)=>{
    if(store.getters.getAccessToken){
        next()
    }
    else{
        next('/Login')
    }
}