// main.js

// O menu ativo e marcado no servidor (base.html), mas links para rotas
// filhas (/clientes/3/editar) nao batem com href exato; reforca pelo path.
document.addEventListener('DOMContentLoaded', function () {
    const path = window.location.pathname;
    document.querySelectorAll('nav a').forEach(function (link) {
        if (link.classList.contains('ativo')) {
            return;
        }
        const href = new URL(link.href, window.location.origin).pathname;
        if (href !== '/' && path.startsWith(href)) {
            link.classList.add('ativo');
        }
    });

    // Confirmacao de exclusao vive no onsubmit de cada template.
});
