import { createToaster } from '@meforma/vue-toaster'
export default function showToast (message,type="error"){
    const toaster = createToaster()
    if(type=='error'){
      toaster.error(message,{
        position:"top-right",
        dismissible: true}); 
    }
    else{
      toaster.success(message,{
        position:"top-right",
        dismissible: true})
    }
  }