// Oczekiwanie na pełne załadowanie strony
document.addEventListener('DOMContentLoaded', function() {

    // --- 1. Potwierdzenie Wylogowania (dla poprawy user experience) ---
    // Pobranie przycisku wylogowania
    const logoutForm = document.querySelector('form[action$="/logout/"]');

    if (logoutForm) {
        logoutForm.addEventListener('submit', function(event) {
            // Wyświetlenie okna dialogowego z pytaniem
            if (!confirm('Czy na pewno chcesz się wylogować?')) {
                // Jeśli użytkownik naciśnie "Anuluj", zatrzymaj wysłanie formularza
                event.preventDefault();
            }
        });
    }

    // --- 2. Prosta Animacja (przykład na stronie gry) ---
    const mainHeader = document.querySelector('.content-container h1');

    if (mainHeader) {
        // Dodanie klasy po krótkiej chwili, co można wykorzystać w CSS do animacji
        setTimeout(() => {
            mainHeader.classList.add('fade-in-active');
        }, 100);
    }
});