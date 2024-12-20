document.addEventListener('DOMContentLoaded', () => {

    option = {
              method: 'GET',
              headers: {'X-Requested-With': 'XMLHttpRequest'}};

    const searchForm = document.getElementById('search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(event) {
            event.preventDefault(); // предотвращаем обычную отправку формы

            const query = searchForm.querySelector('input[name="q"]').value;

            // Обновляем параметры URL
            const url = new URL(window.location.href);
            url.searchParams.set('q', query);
            history.pushState({}, '', url);

            // Отправляем запрос через fetch
            fetch(url, option)
                .then(response => response.text()) // Получаем HTML-контент
                .then(data => {
                    document.querySelector('.product-list').innerHTML = data; // Обновляем список товаров
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        });
    }
}