document.addEventListener('DOMContentLoaded', () => {

     option = {
              method: 'GET',
              headers: {'X-Requested-With': 'XMLHttpRequest'}};

    // Фильтрация по цене
    const price_form = document.getElementById('price-filter');
    if (price_form) {
        price_form.addEventListener('submit', function(event) {
            event.preventDefault(); // предотвращаем обычную отправку формы

            const minPrice = document.querySelector('input[name="min_price"]').value;
            const maxPrice = document.querySelector('input[name="max_price"]').value;

            // Обновляем параметры URL
            const url = new URL(window.location.href);
            url.searchParams.set('min_price', minPrice);
            url.searchParams.set('max_price', maxPrice);
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

    // Фильтрация по категории
    document.querySelectorAll('.category-filter').forEach(function(categoryLink) {
        categoryLink.addEventListener('click', function(event) {
            event.preventDefault(); // предотвращаем переход по ссылке

            const selectedItem = document.querySelector('li.selected');
            if (selectedItem) {
                selectedItem.classList.remove('selected');
            }

            categoryLink.closest('li').classList.add('selected'); // Добавляем класс 'selected'

            const categorySlug = categoryLink.dataset.slug;
            const url = new URL(window.location.href);
            url.searchParams.set('category_slug', categorySlug);
            history.pushState({}, '', url);

            fetch(url, option)
                .then(response => response.text()) // Получаем HTML-контент
                .then(data => {
                    document.querySelector('.product-list').innerHTML = data; // Обновляем список товаров
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        });
    });
});
