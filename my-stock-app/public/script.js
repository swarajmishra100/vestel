document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('.stock-form');
  const submitButton = document.querySelector('.submit-button');
  const clearButton = document.querySelector('.clear-button');
  const tickerInput = document.getElementById('ticker');

  form.addEventListener('submit', (e) => {
      e.preventDefault();
      submitButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
      submitButton.disabled = true;

      // Submit the form
      form.submit();
  });

  clearButton.addEventListener('click', () => {
      tickerInput.value = '';
      tickerInput.focus();
  });


  const inputFields = document.querySelectorAll('.input-field');
  inputFields.forEach(input => {
      input.addEventListener('focus', () => {
          input.parentElement.classList.add('focused');
      });
      input.addEventListener('blur', () => {
          if (input.value === '') {
              input.parentElement.classList.remove('focused');
          }
      });
  });
});