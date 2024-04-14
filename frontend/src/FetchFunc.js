import store from "./store/index.js";
import axios from "axios";

async function FetchFunction({ url, init_obj, authRequired }){
    if(url === undefined){
        throw Error('Url Required')
    }
    if(init_obj === undefined){
        init_obj = {}
    }
    if(authRequired === undefined){
        authRequired = false
    }
    if(authRequired === true){
        if(init_obj.headers === undefined){
            init_obj.headers = {
                'Authentication-token': store.getters.getToken
            }
        }else{
            init_obj.headers['Authentication-token'] = store.getters.getToken
        }
    }

    const response = await fetch(url, init_obj).catch((err) => {
        throw Error(err)
    })

    if(response){
        if(response.ok){
            const data = await response.json().catch((err) => {
                throw Error(err)
            })
            if(data){
                return data
            }
        }else{
            throw Error(response)
        }
    }
}

async function FetchFunction2({ options, authRequired }){
    

    if(options === undefined){
        options = {}

    }

    if(authRequired === undefined){
        authRequired = false
    }
    if(authRequired === true){
        if(options.headers === undefined){
            options.headers = {
                'Authentication-token': store.getters.getToken
            }
        }else{
            options.headers['Authentication-token'] = store.getters.getToken
        }
    } 

    let response = await axios(options)

    let data = response.data
    return data
    

    
}

export { FetchFunction, FetchFunction2 }