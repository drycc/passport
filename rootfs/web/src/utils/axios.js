import axios from 'axios'
import { ElLoading, ElMessage } from 'element-plus'
import {getCookie} from "./array";

axios.defaults.baseURL = process.env.VUE_APP_BASE_URL
axios.defaults.withCredentials = true
axios.defaults.headers.post['Content-Type'] = 'application/json'
const loadingToast = [];

axios.interceptors.request.use(
    (config)=>{
    loadingToast.push(ElLoading.service({
      lock: true,
      text: "Loading...",
      background: "rgba(0, 0, 0, 0.2)",
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
        loadingToast.pop().close();
      }
      if ([200, 201, 204].indexOf(response.status) >= 0) {
        return Promise.resolve(response);
      } else {
        return Promise.reject(response);
      }
    },
    error => {
      if (loadingToast.length > 0) {
        loadingToast.pop().close();
      }
      if (error.response && error.response.status) {
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
              break;
          case 404:
            console.log('error.response: ', error.response)
              if(error.response.data){
                ElMessage({
                    message: error.response.data.replace("\"","").replace("\"",""),
                    type: "error",
                    duration: 1500,
                });
              }else {
                ElMessage({
                    message: 'The request does not exist.',
                    type: "error",
                    duration: 1500,
                });
              }
            break;
          case 400:
            console.log('error.response: ', error.response)
              if(error.response.data.detail){
                ElMessage({
                    message: error.response.data.detail.replace("\"","").replace("\"",""),
                    type: "error",
                    duration: 1500,
                });
              }else {
                ElMessage({
                    message: 'The request parameter error',
                    type: "error",
                    duration: 1500,
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
        return Promise.reject(error);
      }
      return Promise.reject(error);
    }
);

export default axios
