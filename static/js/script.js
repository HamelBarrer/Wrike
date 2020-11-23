// Inicializador de sidenav
document.addEventListener('DOMContentLoaded', () => {
    let elems = document.querySelectorAll('.sidenav');
    let instances = M.Sidenav.init(elems);
});

// Inicializador del select
document.addEventListener('DOMContentLoaded', () => {
    var elems = document.querySelectorAll('select');
    var instances = M.FormSelect.init(elems);
});