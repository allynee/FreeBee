import {store} from '../store/index.js'
export default(to,from,next)=>{
    if(store.getters.getAccessToken){
        next()
    }
    else{
        next('/Login')
    }
    console.log(store.state.corporateName)
    if(store.state.corporateName){
        next('/corporatehomepage')
    }
    else{
        next()
    }
}   
