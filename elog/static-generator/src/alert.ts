import Swal from 'sweetalert2/dist/sweetalert2.js';
import successIconHtml from './icons/success.svg?raw';
import warnIconHtml from './icons/warning.svg?raw';
import alertIconHtml from './icons/alert.svg?raw';
import infoIconHtml from './icons/info.svg?raw';
import './alert.css'

const commonOptions = {
    toast: true,
    timer: 5500,
    position: 'bottom-end',
    showConfirmButton: false,
    showCloseButton: true,
    timerProgressBar: true,
    customClass: {
        timerProgressBar: 'popup-timer-progress-bar'
    }
}

const Notification = {
    info: Swal.mixin({
        ...commonOptions,
        iconHtml: infoIconHtml,
        customClass: {
            popup: 'info-popup',
        },
    }),
    alert: Swal.mixin({
        ...commonOptions,
        iconHtml: alertIconHtml,
        customClass: {
            popup: 'alert-popup',
        },
    }),
    warn: Swal.mixin({
        ...commonOptions,
        iconHtml: warnIconHtml,
        customClass: {
            popup: 'warn-popup',
        }
    }),
    success: Swal.mixin({
        ...commonOptions,
        iconHtml: successIconHtml,
        customClass: {
            popup: 'success-popup',
        },
    }),

};

export default Notification;
