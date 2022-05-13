import axios from 'axios'
import { Toast } from 'vant'
import {getCookie} from "./array";

axios.defaults.baseURL = process.env.VUE_APP_BASE_URL
axios.defaults.withCredentials = true
axios.defaults.headers.post['Content-Type'] = 'application/json'
const loadingToast = [];

axios.interceptors.request.use(
    (config)=>{
        loadingToast.push(Toast.loading({
            duration: 0,
            forbidClick: true,
            message: "Loading..."
        }));
        let csrftoken = getCookie('csrftoken')
        if(csrftoken){
            config.headers['X-CSRFToken'] = csrftoken;
        }
        return config
    }
)

axios.interceptors.response.use(
    response => {
      if (loadingToast.length > 0) {
        loadingToast.pop().clear();
      }
      if ([200, 201, 204].indexOf(response.status) >= 0) {
        return Promise.resolve(response);
      } else {
        return Promise.reject(response);
      }
    },
    error => {
      if (loadingToast.length > 0) {
        loadingToast.pop().clear();
      }
      if (error.response.status) {
        switch (error.response.status) {
          case 401:
            window.location.replace("/user/login/");
            break;
          case 403:
              console.log("error.response.data.detail: ", error.response.data.detail)
              if(error.response.data.detail.indexOf('Authentication credentials were not provided.') >= 0){
                  window.location.replace("/user/login/");
                  break;
              }else {
                  console.log({
                      message: error.response.data.message,
                      duration: 1500,
                      forbidClick: true
                  });
              }
          case 404:
            console.log('error.response: ', error.response)
              if(error.response.data){
                  Toast({
                      message: error.response.data.replace("\"","").replace("\"",""),
                      duration: 1500,
                      forbidClick: true
                  });
              }else {
                  Toast({
                      message: 'The request does not exist.',
                      duration: 1500,
                      forbidClick: true
                  });
              }
            break;
          case 400:
            console.log('error.response: ', error.response)
              if(error.response.data.detail){
                  Toast({
                      message: error.response.data.detail.replace("\"","").replace("\"",""),
                      duration: 1500,
                      forbidClick: true
                  });
              }else {
                  Toast({
                      message: 'The request parameter error',
                      duration: 1500,
                      forbidClick: true
                  });
              }
            break;
          // other error
          default:
            console.log({
              message: error.response.data.message,
              duration: 1500,
              forbidClick: true
            });
        }
        return Promise.reject(error.response);
      }
    }
);

export default axios
