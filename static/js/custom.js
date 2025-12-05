// Oczekiwanie na pełne załadowanie strony
document.addEventListener('DOMContentLoaded', function() {

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
});