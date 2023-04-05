import {store} from '../store/index.js'
export default(to,from,next)=>{
    if(!store.state.corporateName){
        next()
    }
    else{
        next('/')
    }
}   
