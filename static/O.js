    let fromCurrency = "USD";
    let toCurrency = "IDR";

    // Elements
    const fromBtn = document.getElementById("from-currency");
    const toBtn = document.getElementById("to-currency");
    const fromList = document.getElementById("from-currency-list");
    const toList = document.getElementById("to-currency-list");
    const fromText = document.getElementById("from-currency-text");
    const toText = document.getElementById("to-currency-text");
    const amountInput = document.getElementById("amount");
    const form = document.getElementById("converter-form");
    const swapBtn = document.getElementById("swap-btn");
    const amountError = document.getElementById("amount-error");
    const convertButton = document.getElementById("convert-button");
    
    // New elements for conversion result
    const conversionResult = document.getElementById("conversion-result");
    const rateText = document.getElementById("rate-text");
    const convertedAmount = document.getElementById("converted-amount");
    const inverseRateText = document.getElementById("inverse-rate-text");
    const linkFrom = document.getElementById("link-from");
    const linkTo = document.getElementById("link-to");
    const lastUpdated = document.getElementById("last-updated");
    const loadingDots = document.getElementById("loading-dots");

    // Set currency display and update aria attributes
    function setFromCurrency(code, name, flag) {
      fromCurrency = code;
      fromText.textContent = `${code} - ${name}`;
      fromBtn.querySelector("img").src = `https://flagcdn.com/w40/${flag}.png`;
      fromBtn.querySelector("img").alt = `Flag of ${name}`;
      fromBtn.setAttribute("aria-expanded", "false");
    }
    
    function setToCurrency(code, name, flag) {
      toCurrency = code;
      toText.textContent = `${code} - ${name}`;
      toBtn.querySelector("img").src = `https://flagcdn.com/w40/${flag}.png`;
      toBtn.querySelector("img").alt = `Flag of ${name}`;
      toBtn.setAttribute("aria-expanded", "false");
    }

    // Toggle dropdown visibility
    function toggleDropdown(list, button) {
      const isOpen = list.classList.contains("hidden") === false;
      closeDropdowns();
      if (!isOpen) {
        list.classList.remove("hidden");
        button.setAttribute("aria-expanded", "true");
        list.focus();
      }
    }
    
    // Close all dropdowns
    function closeDropdowns() {
      fromList.classList.add("hidden");
      toList.classList.add("hidden");
      fromBtn.setAttribute("aria-expanded", "false");
      toBtn.setAttribute("aria-expanded", "false");
    }

    // Swap currencies
    function swapCurrencies() {
      const tempCurrency = fromCurrency;
      const tempName = fromText.textContent;
      const tempFlag = fromBtn.querySelector("img").src.split('/').pop().replace('.png', '');
      
      setFromCurrency(toCurrency, toText.textContent.split(' - ')[1], toBtn.querySelector("img").src.split('/').pop().replace('.png', ''));
      setToCurrency(tempCurrency, tempName.split(' - ')[1], tempFlag);
      conversionResult.classList.add("hidden");
    }

    // Show loading state
    function showLoading() {
      conversionResult.classList.remove("hidden");
      loadingDots.classList.remove("hidden");
      convertedAmount.innerHTML = `
        <span class="loading-dots" id="loading-dots">
          <span></span>
          <span></span>
          <span></span>
        </span>
      `;
      rateText.textContent = "Converting...";
      inverseRateText.textContent = "";
    }

    // Show error message
    function showError(message) {
      rateText.textContent = "";
      convertedAmount.innerHTML = `<span class="text-red-600">${message}</span>`;
      inverseRateText.textContent = "";
      lastUpdated.textContent = "Please try again later.";
      conversionResult.classList.remove("hidden");
      loadingDots.classList.add("hidden");
    }

    // Event listeners for dropdown buttons
    fromBtn.addEventListener("click", () => toggleDropdown(fromList, fromBtn));
    toBtn.addEventListener("click", () => toggleDropdown(toList, toBtn));

    // Close dropdowns on outside click
    document.addEventListener("click", (e) => {
      if (
        !fromBtn.contains(e.target) &&
        !fromList.contains(e.target) &&
        !toBtn.contains(e.target) &&
        !toList.contains(e.target) &&
        !swapBtn.contains(e.target)
      ) {
        closeDropdowns();
      }
    });

    // Currency option selection
    document.querySelectorAll('.currency-option').forEach(option => {
      option.addEventListener('click', function() {
        const code = this.getAttribute('data-code');
        const name = this.getAttribute('data-name');
        const flag = this.getAttribute('data-flag');
        
        if (this.parentElement.id === 'from-currency-list') {
          setFromCurrency(code, name, flag);
        } else {
          setToCurrency(code, name, flag);
        }
        
        closeDropdowns();
        amountInput.focus();
      });
    });

    // Keyboard navigation for dropdown buttons
    fromBtn.addEventListener("keydown", (e) => {
      if (e.key === "ArrowDown" || e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        toggleDropdown(fromList, fromBtn);
      }
    });
    
    toBtn.addEventListener("keydown", (e) => {
      if (e.key === "ArrowDown" || e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        toggleDropdown(toList, toBtn);
      }
    });

    // Swap button click and keyboard
    swapBtn.addEventListener("click", () => {
      swapCurrencies();
      amountInput.focus();
    });
    
    swapBtn.addEventListener("keydown", (e) => {
      if (e.key === "Enter" || e.key === " ") {
        e.preventDefault();
        swapCurrencies();
        amountInput.focus();
      }
    });
    
    // Form submit handler
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      amountError.classList.add("hidden");
      
      const amount = parseFloat(amountInput.value);
      if (isNaN(amount) || amount <= 0) {
        amountError.classList.remove("hidden");
        amountInput.focus();
        return;
      }
      
      if (fromCurrency === toCurrency) {
        showError("Please select two different currencies.");
        return;
      }
      
      showLoading();
      
      try {
        const response = await fetch('/convert', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            amount: amount,
            fromCurrency: fromCurrency,
            toCurrency: toCurrency
          })
        });
        
        const data = await response.json();
        
        if (data.success) {
          rateText.textContent = data.rateText;
          convertedAmount.innerHTML = `
            <span class="mr-1">${data.convertedAmount}</span>
            <span>${data.currencyName}</span>
          `;
          inverseRateText.textContent = data.inverseRateText;
          linkFrom.textContent = data.fromCurrencyName;
          linkTo.textContent = data.toCurrencyName;
          lastUpdated.textContent = data.lastUpdated;
          loadingDots.classList.add("hidden");
        } else {
          showError(data.error);
        }
      } catch (error) {
        showError("Sorry, we couldn't fetch the conversion rate.");
      }
    });
