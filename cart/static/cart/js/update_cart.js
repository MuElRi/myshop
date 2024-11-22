document.addEventListener('DOMContentLoaded', () => {
    const csrftoken = Cookies.get('csrftoken');

    const updateCartContainers = document.querySelectorAll('.update-cart');
    updateCartContainers.forEach(container => {
        container.addEventListener('submit', function (e) {
            e.preventDefault(); // Останавливаем стандартное поведение формы

            const form = container.querySelector('form');
            const url = form.action;
            const row = container.closest('tr'); // Находим строку товара

            const formData = new FormData(form);
            const options = {
                method: 'POST',
                body: formData,
                headers: { 'X-CSRFToken': csrftoken },
                mode: 'same-origin'
            };
            console.log(form)
            fetch(url, options)
                .then(response => response.text())
                .then(html => {
                     // Проверяем значение количества, если 0, удаляем строку
                    console.log(form)
//                    const quantityInput = container.querySelector('input[name="quantity"]');
//                    if (quantityInput && parseInt(quantityInput.value) === 0) {
//                        row.remove(); // Удаляем строку из таблицы
//                    }
                    if (html === ""){
                        row.remove();
                    }
                    else{
                        // Обновляем контейнер с формой
                        container.innerHTML = html;
                    }
                    // Обновляем общую сумму корзины
                    updateCartTotal();
                })
                .catch(error => console.error('Ошибка:', error));
        });
    });

    // Функция для обновления общей суммы корзины
    function updateCartTotal() {
        const totalField = document.querySelector('tr.total .num');
        if (totalField) {
            let total = 0;
            document.querySelectorAll('tbody tr').forEach(row => {
                const priceField = row.querySelector('td.num:last-child');
                if (priceField) {
                    total += parseFloat(priceField.textContent.replace('$', '')) || 0;
                }
            });
            totalField.textContent = `$${total.toFixed(2)}`;
        }
    }
});
