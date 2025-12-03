document.addEventListener('DOMContentLoaded', function() {
    // 1. Pobierz elementy
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');

    // 2. Dodaj nasłuchiwanie kliknięcia, jeśli elementy istnieją
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            // Przełącza klasę 'active', która jest używana w CSS do pokazania/ukrycia menu
            navMenu.classList.toggle('active');

            // Opcjonalnie: Zmienia przycisk toggle na 'X' lub inny stan
            navToggle.classList.toggle('is-open');
        });
    }

    // 3. TUTAJ MOŻESZ DODAĆ SWOJE SKRYPTY
    // Np. prostą walidację formularza lub efekty wizualne.

});