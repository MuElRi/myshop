document.addEventListener('DOMContentLoaded', (event) => {
    const csrftoken = Cookies.get('csrftoken');

    // Делегирование событий для всех форм корзины
    document.querySelector('.product-list').addEventListener('submit', function(event) {
        const form = event.target;
        if (form.classList.contains('update-cart')) {
            event.preventDefault(); // Останавливаем стандартное поведение формы

            const url = form.action;
            const button = event.submitter; // Кнопка, вызвавшая событие
            const action = button.value;

            const formData = new FormData(form);
            formData.append("action", action);

            const options = {
                method: 'POST',
                body: formData,
                headers: { 'X-CSRFToken': csrftoken },
                mode: 'same-origin'
            };

            fetch(url, options)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        if (data.quantity !== 0) {
                            form.innerHTML = `
                                <input type="submit" value="-" class="btn btn-update">
                                <input type="hidden" name="product_id" value="${data.product_id}">
                                <input type="number" name="quantity" value="${data.quantity}" readonly>
                                <input type="submit" value="+" class="btn btn-update">
                              `;
                        } else {
                            form.innerHTML = `
                                <input type="hidden" name="product_id" value="${data.product_id}">
                                <input type="submit" value="Add" class="btn btn-add-product">
                              `;
                        }
                        updateCartInfo(data);
                    } else {
                        alert(data.message || 'Произошла ошибка. Попробуйте снова.');
                    }
                })
                .catch(error => {
                    alert('Не удалось соединиться с сервером. Проверьте подключение.');
                });
        }
    });
});



//document.addEventListener('DOMContentLoaded', (event) => {
//    const csrftoken = Cookies.get('csrftoken');
//
//    const updateCartContainers = document.querySelectorAll('.update-cart')
//    updateCartContainers.forEach(container=> {
//        container.addEventListener('submit', function(e) {
//
//            e.preventDefault();  // Останавливаем стандартное поведение формы
//            const form = container.querySelector('form')
//            const url = form.action
//            console.log(url)
//            var formData = new FormData(form)
//
//            options = {
//                method: 'POST',
//                body: formData,
//                headers:{ 'X-CSRFToken': csrftoken },
//                mode: 'same-origin'
//            }
//
//            fetch(url, options)
//                .then(response => response.text())
//                .then(html => {
//                    console.log(3)
//                    container.innerHTML = html
//                })
//                .catch(error => console.error('Ошибка:', error));
//        });
//    });

        // Получаем все кнопки "add-to-cart"
//    const addToCartButtons = document.querySelectorAll('a.add-to-cart');
//
//    addToCartButtons.forEach(addButton => {
//        addButton.addEventListener('click', function(e) {
//            e.preventDefault();
//
//            const url = addButton.dataset.url;
//            var options = {
//                method: 'POST',
//                headers: { 'X-CSRFToken': csrftoken },
//                mode: 'same-origin'
//            };
//
//            // Добавляем данные в тело запроса
//            var formData = new FormData();
//            formData.append('id', addButton.dataset.id);
//            formData.append('action', addButton.dataset.action);
//            options['body'] = formData;
//
//            // Отправляем HTTP-запрос
//            fetch(url, options)
//                .then(response => response.json())
//                .then(data => {
//                    if (data['status'] === 'ok') {
//                        var previousAction = addButton.dataset.action;
//
//                        // Переключаем текст кнопки и data-action
//                        var action = previousAction === 'add' ? 'remove' : 'add';
//                        addButton.dataset.action = action;
//                        addButton.innerHTML = action === 'add' ? 'Add to cart' : 'In cart';
//                    }
//                });
//        });
//    });