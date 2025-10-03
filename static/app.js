let fromCurrency = "USD";
let toCurrency = "IDR";

// Elements
const fromBtn = document.getElementById("from-currency");
const toBtn = document.getElementById("to-currency");
const fromList = document.getElementById("from-currency-list");
const toList = document.getElementById("to-currency-list");
const fromSearch = document.getElementById('from-currency-search');
const toSearch = document.getElementById('to-currency-search');
const fromText = document.getElementById("from-currency-text");
const toText = document.getElementById("to-currency-text");
const amountInput = document.getElementById("amount");
const form = document.getElementById("converter-form");
const swapBtn = document.getElementById("swap-btn");
const amountError = document.getElementById("amount-error");
const convertButton = document.getElementById("convert-button");

// Elements untuk search

// New elements for conversion result
const conversionResult = document.getElementById("conversion-result");
const rateText = document.getElementById("rate-text");
const convertedAmount = document.getElementById("converted-amount");
const inverseRateText = document.getElementById("inverse-rate-text");
const linkFrom = document.getElementById("link-from");
const linkTo = document.getElementById("link-to");
const lastUpdated = document.getElementById("last-updated");
const loadingDots = document.getElementById("loading-dots");

// Variabel global untuk tab dan berita
const tabs = document.querySelectorAll('[role="tab"]');
const tabContents = document.querySelectorAll('.tab-content');
const newsContainer = document.getElementById('news-container');
const refreshNewsBtn = document.getElementById('refresh-news');

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

// Fungsi untuk filter mata uang berdasarkan pencarian
function filterCurrencies(searchTerm, list) {
  const options = list.querySelectorAll('.currency-option');
  const searchLower = searchTerm.toLowerCase();
  
  options.forEach(option => {
    const code = option.getAttribute('data-code').toLowerCase();
    const name = option.getAttribute('data-name').toLowerCase();
    const text = option.textContent.toLowerCase();
    
    if (code.includes(searchLower) || name.includes(searchLower) || text.includes(searchLower)) {
      option.classList.remove('hidden');
    } else {
      option.classList.add('hidden');
    }
  });
}



const audio = document.getElementById("audio");
    const playBtn = document.getElementById("playBtn");
    const canvas = document.getElementById("visualizer");
    const ctx = canvas.getContext("2d");
//    const nowPlaying = document.getElementById("nowPlaying");

    // 🎶 Playlist di JS (tanpa UI)
    const playlist = [
      "/static/asset/music/1.mp3",
      "/static/asset/music/2.mp3",
      "/static/asset/music/3.mp3",
      "/static/asset/music/4.mp3",
      "/static/asset/music/5.mp3",
      "/static/asset/music/6.mp3"
    ];

    let audioCtx, analyser, source, dataArray;

    // Fungsi pilih lagu random
    function getRandomTrack() {
      const index = Math.floor(Math.random() * playlist.length);
      return playlist[index];
    }

    // Load track
//     function loadTrack(src) {
//      audio.src = src;
//      nowPlaying.textContent = "Now Playing: " + src.split("/").pop();
//    }

    playBtn.addEventListener("click", () => {
      if (!audioCtx) {
        audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        analyser = audioCtx.createAnalyser();
        source = audioCtx.createMediaElementSource(audio);
        source.connect(analyser);
        analyser.connect(audioCtx.destination);
        analyser.fftSize = 2048;
        dataArray = new Uint8Array(analyser.fftSize);

        draw();
      }
function loadTrack(src) {
  audio.src = src;
}
      if (audio.paused) {
        // kalau audio belum pernah dimainkan, load random dulu
        if (!audio.src || audio.src === window.location.href) {
          loadTrack(getRandomTrack());
        }
        audio.play();
        playBtn.textContent = "";
      } else {
        audio.pause();
        playBtn.textContent = "▷";
      }
    });

    // Auto play lagu random berikutnya setelah selesai
    audio.addEventListener("ended", () => {
      loadTrack(getRandomTrack());
      audio.play();
    });

    // Visualizer function
    function draw() {
      requestAnimationFrame(draw);
      analyser.getByteTimeDomainData(dataArray);

      ctx.clearRect(0, 0, canvas.width, canvas.height);

      ctx.lineWidth = 1.5;
      ctx.strokeStyle = "white";
      ctx.beginPath();

      let sliceWidth = canvas.width * 1.0 / dataArray.length;
      let x = 0;

      for (let i = 0; i < dataArray.length; i++) {
        let v = dataArray[i] / 128.0;
        let y = v * canvas.height / 2;

        if (i === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }
        x += sliceWidth;
      }

      ctx.lineTo(canvas.width, canvas.height / 2);
      ctx.stroke();
    }
    
    
    

// Fungsi untuk reset pencarian
function resetSearch(list) {
  const searchInput = list.querySelector('input[type="text"]');
  const options = list.querySelectorAll('.currency-option');
  
  if (searchInput) {
    searchInput.value = '';
  }
  
  options.forEach(option => {
    option.classList.remove('hidden');
    option.style.order = '';
  });
}

// Fungsi untuk navigasi keyboard pada dropdown dengan search
function setupKeyboardNavigation(list, searchInput) {
  let currentIndex = -1;
  
  function getVisibleOptions() {
    return Array.from(list.querySelectorAll('.currency-option:not(.hidden)'));
  }
  
  function resetHighlight() {
    const options = getVisibleOptions();
    options.forEach(option => option.classList.remove('highlight'));
    currentIndex = -1;
  }
  
  function highlightOption(index) {
    const options = getVisibleOptions();
    resetHighlight();
    if (index >= 0 && index < options.length) {
      options[index].classList.add('highlight');
      options[index].scrollIntoView({ block: 'nearest' });
      currentIndex = index;
    }
  }
  
  searchInput.addEventListener('keydown', (e) => {
    const visibleOptions = getVisibleOptions();
    
    switch(e.key) {
      case 'ArrowDown':
        e.preventDefault();
        highlightOption((currentIndex + 1) % visibleOptions.length);
        break;
      case 'ArrowUp':
        e.preventDefault();
        highlightOption((currentIndex - 1 + visibleOptions.length) % visibleOptions.length);
        break;
      case 'Enter':
        e.preventDefault();
        if (currentIndex >= 0 && currentIndex < visibleOptions.length) {
          visibleOptions[currentIndex].click();
        }
        break;
      case 'Escape':
        closeDropdowns();
        break;
    }
  });
  
  // Reset highlight ketika mengetik
  searchInput.addEventListener('input', () => {
    resetHighlight();
  });
  
  // Highlight pada hover
  list.addEventListener('mouseover', (e) => {
    const option = e.target.closest('.currency-option');
    if (option && !option.classList.contains('hidden')) {
      resetHighlight();
      const visibleOptions = getVisibleOptions();
      const index = visibleOptions.indexOf(option);
      if (index !== -1) {
        option.classList.add('highlight');
        currentIndex = index;
      }
    }
  });
}

// Fungsi pencarian yang lebih cerdas dengan prioritaskan kode mata uang
function smartCurrencySearch(searchTerm, list) {
  const options = list.querySelectorAll('.currency-option');
  const searchLower = searchTerm.toLowerCase().trim();
  
  if (!searchLower) {
    options.forEach(option => {
      option.classList.remove('hidden');
      option.style.order = '';
    });
    return;
  }
  
  const matchedOptions = [];
  
  options.forEach(option => {
    const code = option.getAttribute('data-code').toLowerCase();
    const name = option.getAttribute('data-name').toLowerCase();
    
    // Prioritaskan pencarian berdasarkan kode mata uang
    const codeMatch = code === searchLower;
    const codeStartsWith = code.startsWith(searchLower);
    const nameMatch = name.includes(searchLower);
    
    if (codeMatch || codeStartsWith || nameMatch) {
      option.classList.remove('hidden');
      
      // Tentukan skor relevansi
      let score = 3;
      if (codeMatch) score = 1;
      else if (codeStartsWith) score = 2;
      
      matchedOptions.push({ option, score });
    } else {
      option.classList.add('hidden');
      option.style.order = '';
    }
  });
  
  // Sort berdasarkan relevansi
  matchedOptions.sort((a, b) => a.score - b.score);
  
  // Apply order
  matchedOptions.forEach((item, index) => {
    item.option.style.order = item.score;
  });
}

// Toggle dropdown visibility
function toggleDropdown(list, button) {
  const isOpen = list.classList.contains("hidden") === false;
  closeDropdowns();
  if (!isOpen) {
    list.classList.remove("hidden");
    button.setAttribute("aria-expanded", "true");
    
    // Reset pencarian saat dropdown dibuka
    resetSearch(list);
    
    // Fokus ke input search
    const searchInput = list.querySelector('input[type="text"]');
    if (searchInput) {
      setTimeout(() => {
        searchInput.focus();
        setupKeyboardNavigation(list, searchInput);
      }, 10);
    }
  }
}

// Close all dropdowns
function closeDropdowns() {
  fromList.classList.add("hidden");
  toList.classList.add("hidden");
  fromBtn.setAttribute("aria-expanded", "false");
  toBtn.setAttribute("aria-expanded", "false");
  
  // Reset pencarian saat dropdown ditutup
  resetSearch(fromList);
  resetSearch(toList);
}

// Swap currencies
function swapCurrencies() {
  const tempCurrency = fromCurrency;
  const tempText = fromText.textContent;
  const tempFlag = fromBtn.querySelector("img").src.split('/').pop().replace('.png', '');
  
  const fromName = toText.textContent.split(' - ')[1];
  const toName = tempText.split(' - ')[1];
  const toFlag = toBtn.querySelector("img").src.split('/').pop().replace('.png', '');
  
  setFromCurrency(toCurrency, fromName, toFlag);
  setToCurrency(tempCurrency, toName, tempFlag);
  
  // Jika ada hasil konversi, swap juga amount
  if (!conversionResult.classList.contains('hidden')) {
    const currentAmount = amountInput.value;
    if (currentAmount && !isNaN(parseFloat(currentAmount))) {
      form.dispatchEvent(new Event('submit'));
    }
  }
}

// Show loading state
function showLoading() {
  conversionResult.classList.remove("hidden");
  loadingDots.classList.remove("hidden");
  rateText.textContent = "Converting...";
  inverseRateText.textContent = "";
  convertedAmount.innerHTML = '';
  
  // Tambahkan loading dots
  const loadingHTML = `
    <span class="loading-dots">
      <span></span>
      <span></span>
      <span></span>
    </span>
  `;
  convertedAmount.innerHTML = loadingHTML;
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

// Fungsi untuk beralih tab - HANYA SATU DEKLARASI
function switchTab(tabId) {
  // Update tabs
  tabs.forEach(tab => {
    const isSelected = tab.getAttribute('data-tab') === tabId;
    tab.setAttribute('aria-selected', isSelected.toString());
    if (isSelected) {
      tab.classList.add('text-blue-600', 'bg-white');
      tab.classList.remove('text-gray-500', 'bg-transparent');
    } else {
      tab.classList.remove('text-blue-600', 'bg-white');
      tab.classList.add('text-gray-500', 'bg-transparent');
    }
  });
tabContents.forEach(content => {
    content.classList.toggle('active', content.id === `content-${tabId}`);
  });

  // Jika tab News dipilih, muat berita
  if (tabId === 'news') {
    loadNews();
  }
}

// Fungsi untuk menampilkan skeleton loading
function showSkeletonLoading() {
  newsContainer.innerHTML = `
    <div class="space-y-4">
      ${Array.from({ length: 5 }, (_, i) => `
        <div class="bg-white rounded-xl p-4 border border-gray-200 animate-pulse">
          <div class="h-6 bg-gray-200 rounded w-3/4 mb-3"></div>
          <div class="h-4 bg-gray-200 rounded w-full mb-2"></div>
          <div class="h-4 bg-gray-200 rounded w-5/6 mb-3"></div>
          <div class="flex justify-between items-center">
            <div class="h-3 bg-gray-200 rounded w-1/4"></div>
            <div class="h-3 bg-gray-200 rounded w-1/5"></div>
          </div>
        </div>
      `).join('')}
    </div>
  `;
}

// Fungsi untuk memuat berita
async function loadNews() {
  showSkeletonLoading();

  try {
    const response = await fetch('/get_news');
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();

    // Hapus setTimeout untuk response langsung
    setTimeout(() => {
      displayNews(data.articles);
    }, 10);
  } catch (error) {
    console.error('Error loading news:', error);
    newsContainer.innerHTML = `
      <div class="text-center py-10">
        <div class="inline-flex items-center justify-center w-16 h-16 bg-red-100 rounded-full mb-4">
          <i class="fas fa-exclamation-triangle text-xl text-red-500"></i>
        </div>
        <h3 class="text-lg font-semibold text-gray-700 mb-2">Failed to Load News</h3>
        <p class="text-gray-500 mb-4">Please check your connection and try again.</p>
        <button class="px-4 py-2 bg-blue-600 text-white rounded-lg flex items-center mx-auto" id="retry-news">
          <i class="fas fa-redo mr-2"></i> Try Again
        </button>
      </div>
    `;
    document.getElementById('retry-news').addEventListener('click', loadNews);
  }
}

// Fungsi untuk menampilkan berita
function displayNews(articles) {
  if (!articles || articles.length === 0) {
    newsContainer.innerHTML = `
      <div class="text-center py-4">
        <div class="inline-flex items-center justify-center w-12 h-12 bg-gray-100 rounded-full mb-2">
          <i class="far fa-newspaper text-lg text-gray-500"></i>
        </div>
        <h3 class="text-md font-semibold text-gray-700 mb-1">No News Available</h3>
        <p class="text-gray-500 text-sm">Check back later for the latest updates.</p>
      </div>
    `;
    return;
  }
  
  newsContainer.innerHTML = articles.map(article => `
    <div class="bg-white rounded-xl p-4 border border-gray-200 mb-4 news-item">
      <h3 class="text-lg font-semibold text-gray-800 mb-2 news-title">${article.title || 'No title'}</h3>
      <p class="text-gray-600 mb-3 news-description">${article.description || 'No description available'}</p>
      <div class="flex justify-between items-center text-xs text-gray-500 news-meta">
        <span class="news-source">${article.source || 'Unknown source'}</span>
        <span class="news-time"><i class="far fa-clock text-xs mr-1"></i>${article.time || 'Unknown time'}</span>
      </div>
      ${article.url && article.url !== '#' ? `
        <div class="mt-3">
          <a href="${article.url}" target="_blank" class="text-blue-600 hover:text-blue-800 font-medium read-more">
            Read full article <i class="fas fa-external-link-alt ml-1 text-xs"></i>
          </a>
        </div>
      ` : ''}
    </div>
  `).join('');
}

// Event listeners for dropdown buttons
fromBtn.addEventListener("click", (e) => {
  e.stopPropagation();
  toggleDropdown(fromList, fromBtn);
});

toBtn.addEventListener("click", (e) => {
  e.stopPropagation();
  toggleDropdown(toList, toBtn);
});

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
    
    if (this.closest('#from-currency-list')) {
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
    console.error('Conversion error:', error);
    showError("Sorry, we couldn't fetch the conversion rate.");
  }
});

// Event listeners untuk tab
tabs.forEach(tab => {
  tab.addEventListener('click', function() {
    const tabId = this.getAttribute('data-tab');
    switchTab(tabId);
  });
});

// Event listener untuk tombol refresh berita
if (refreshNewsBtn) {
  refreshNewsBtn.addEventListener('click', function() {
    const icon = this.querySelector('i');
    icon.classList.add('fa-spin');
    loadNews();
    setTimeout(() => {
      icon.classList.remove('fa-spin');
    }, 1000);
  });
}

// Inisialisasi saat DOM siap
document.addEventListener('DOMContentLoaded', function() {
  // Setup keyboard navigation untuk dropdown
  fromSearch.addEventListener('input', (e) => {
   smartCurrencySearch(e.target.value, fromList);
   setupKeyboardNavigation(fromList, fromSearch);
  });
  
  toSearch.addEventListener('input', (e) => {
   smartCurrencySearch(e.target.value, toList);
   setupKeyboardNavigation(toList, toSearch);
  });;

  // Event listeners untuk tab - HANYA SATU KALI
  tabs.forEach(tab => {
    const tabs = document.querySelectorAll('[role="tab"]');
    tab.addEventListener('click', function() {
      const tabId = this.getAttribute('data-tab');
      switchTab(tabId);
    });
  });

  // Initialize dengan tab Convert aktif
  switchTab('convert');
  
  // Focus ke amount input
  amountInput.focus();
});
