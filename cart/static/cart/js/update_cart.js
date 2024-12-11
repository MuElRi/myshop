document.addEventListener('DOMContentLoaded', (event) => {
    const csrftoken = Cookies.get('csrftoken');

    const forms = document.querySelectorAll('.update-cart')
    forms.forEach(form=> {
        form.addEventListener('submit', function(event) {
            event.preventDefault();  // Останавливаем стандартное поведение формы
            const url = form.action
            const button = event.submitter
            action = button.value

            var formData = new FormData(form)
            formData.append("action", action)

            options = {
                method: 'POST',
                body: formData,
                headers:{ 'X-CSRFToken': csrftoken },
                mode: 'same-origin'
            }
            fetch(url, options)
                .then(response => response.json())
                .then(data => {
                    console.log(3)
                    if (data.success){
                        const row = form.closest('tr'); // Найти строку товара
                        if (data.quantity!==0){
                            form.innerHTML = `
                                <input type="submit" value="-" class="btn btn-update">
                                <input type="hidden" name="product_id" value="${data.product_id}">
                                <input type="number" name="quantity" value="${data.quantity}" readonly>
                                <input type="submit" value="+" class="btn btn-update">
                              `;
                               // Обновить цену продукта
                            const productPriceCell = row.querySelector('.total-product-price');
                            if (productPriceCell) {
                                productPriceCell.textContent = `$${data.total_product_price}`;
                            }
                        }
                        else{
                           row.remove();
                        }
                        // Обновить общую сумму
                        const totalPriceCell = document.querySelector('.total-price');
                        if (totalPriceCell){
                            totalPriceCell.textContent = `₽${data.total_price}`;
                        }
                        const discountCell = document.querySelector('.discount');
                        if (discountCell){
                            discountCell.textContent = `– ₽ ${data.discount}`;
                        }
                        const PriceAfterDiscountCell = document.querySelector('.total-price-after-discount');
                        if (PriceAfterDiscountCell){
                            PriceAfterDiscountCell.textContent = `₽ ${data.total_price_after_discount}`;
                        }

                        updateCartInfo(data)
                    }
                    else{
                         // Ошибка: показываем сообщение пользователю
                        alert(data.message || 'Произошла ошибка. Попробуйте снова.');
                    }
                })
                .catch((error) => {
                     alert('Не удалось соединиться с сервером. Проверьте подключение.');
                });
        });
    });
});





//document.addEventListener('DOMContentLoaded', () => {
//    const csrftoken = Cookies.get('csrftoken');
//
//    const updateCartContainers = document.querySelectorAll('.update-cart');
//    updateCartContainers.forEach(container => {
//        container.addEventListener('submit', function (e) {
//            e.preventDefault(); // Останавливаем стандартное поведение формы
//
//            const form = container.querySelector('form');
//            const url = form.action;
//            const row = container.closest('tr'); // Находим строку товара
//
//            const formData = new FormData(form);
//            const options = {
//                method: 'POST',
//                body: formData,
//                headers: { 'X-CSRFToken': csrftoken },
//                mode: 'same-origin'
//            };
//            console.log(form)
//            fetch(url, options)
//                .then(response => response.text())
//                .then(html => {
//                     // Проверяем значение количества, если 0, удаляем строку
//                    console.log(form)
////                    const quantityInput = container.querySelector('input[name="quantity"]');
////                    if (quantityInput && parseInt(quantityInput.value) === 0) {
////                        row.remove(); // Удаляем строку из таблицы
////                    }
//                    if (html === ""){
//                        row.remove();
//                    }
//                    else{
//                        // Обновляем контейнер с формой
//                        container.innerHTML = html;
//                    }
//                    // Обновляем общую сумму корзины
//                    updateCartTotal();
//                })
//                .catch(error => console.error('Ошибка:', error));
//        });
//    });
//
//    // Функция для обновления общей суммы корзины
//    function updateCartTotal() {
//        const totalField = document.querySelector('tr.total .num');
//        if (totalField) {
//            let total = 0;
//            document.querySelectorAll('tbody tr').forEach(row => {
//                const priceField = row.querySelector('td.num:last-child');
//                if (priceField) {
//                    total += parseFloat(priceField.textContent.replace('$', '')) || 0;
//                }
//            });
//            totalField.textContent = `$${total.toFixed(2)}`;
//        }
//    }
//});
