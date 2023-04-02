import {store} from '../store/index.js'
export default(to,from,next)=>{
    console.log(store.state.corporateName)
    if(!store.state.corporateName){
        next()
    }
    else{
        next('/')
    }
}   
