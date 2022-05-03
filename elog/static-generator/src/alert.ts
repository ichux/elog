// @ts-ignore
import Swal from 'sweetalert2/dist/sweetalert2.js';
import './alert.css'

const commonOptions = {
    toast: true,
    // timer: 3000,
    position: 'top-end',
    showConfirmButton: false,
    timerProgressBar: true,
}

const Notification = {
    warn: Swal.mixin({...commonOptions, icon: 'warning'}),
    info: Swal.mixin({...commonOptions, icon: 'info'}),
    alert: Swal.mixin({...commonOptions, icon: 'error'}),
    success: Swal.mixin({...commonOptions, icon: 'success'}),

};

window.Notification = Notification

export default Notification;