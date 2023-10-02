// custom.js
function toggleOptions(button) {
    var optionsDiv = button.nextElementSibling;
    optionsDiv.style.display = optionsDiv.style.display === 'block' ? 'none' : 'block';
    button.style.display = optionsDiv.style.display === 'block' ? 'none' : 'block';
}

function incrementCounter(button) {
    var counterSpan = button.previousElementSibling; // Get the counter span element
    var counterValue = parseInt(counterSpan.textContent); // Parse the current counter value

    if (!isNaN(counterValue)) {
        counterValue++; // Increment the counter
        counterSpan.textContent = counterValue; // Update the counter display
        counterSpan.style.display = 'inline'; // Show the counter

        // Show the "Add to Cart" button when counter is greater than zero
        var addToCartButton = button.parentNode.querySelector('.add-to-cart-btn');
        addToCartButton.style.display = 'none';
    }
}

function decrementCounter(button) {
    var counterSpan = button.nextElementSibling; // Get the counter span element
    var counterValue = parseInt(counterSpan.textContent); // Parse the current counter value

    if (!isNaN(counterValue) && counterValue > 0) {
        counterValue--; // Decrement the counter
        counterSpan.textContent = counterValue; // Update the counter display

        // Hide the "Add to Cart" button and show the counter when counter is greater than zero
        var cartOptions = button.parentNode.parentNode.querySelector('.cart-options');
        var addToCartButton = button.parentNode.parentNode.querySelector('.add-to-cart-btn');

        cartOptions.style.display = (counterValue === 0) ? 'none' : 'block'; // Show the "Add to Cart" button
        addToCartButton.style.display = (counterValue === 0) ? 'block' : 'none'; // Show the "Add to Cart" button
    }
}
