// Функция для обновления информации о корзине
function updateCartInfo(data) {
    let info = "";

    // Формируем строку информации о корзине
    if (data.total_items === 1) {
        info = `${data.total_items} item, ₽${data.total_price_after_discount}`;
    } else if (data.total_items > 1) {
        info = `${data.total_items} items, ₽${data.total_price_after_discount}`;
    } else {
        info = "Your cart is empty";
    }

    // Обновляем HTML содержимое элемента с классом "cart-info"
    const cartInfo = document.querySelector('.cart-info');
    if (cartInfo) {
        cartInfo.innerHTML = info;
    }
}
