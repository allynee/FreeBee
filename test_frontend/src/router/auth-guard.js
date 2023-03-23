import {store} from '../store/index.js'
export default(to,from,next)=>{
    if(store.getters.getuser){
        next()
    }
    else{
        next('/Login')
    }
}