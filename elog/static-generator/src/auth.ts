import Alpine from "alpinejs";

Alpine.data('auth', () => ({
  tab: 'login',
}));

document.addEventListener("DOMContentLoaded", Alpine.start);
