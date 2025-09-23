const themeBtn = document.getElementById('toggle-theme');
const themeIcon = document.getElementById('theme-icon');

function updateIcon() {
    if (document.documentElement.classList.contains('dark')) {
      themeIcon.innerHTML = `
      <path d="M12 3v1m0 16v1m8.485-8.485h-1m-14.97 0h-1m12.728-7.071l-.707.707m-10.607 0l-.707-.707m12.728 12.728l-.707-.707m-10.607 0l-.707.707M12 5a7 7 0 1 0 7 7"></path>
      `;
    } else {
      themeIcon.innerHTML = `
        <path fill="currentColor" d="M12 3v1m0 16v1m8.485-8.485h-1m-14.97 0h-1m12.728-7.071l-.707.707m-10.607 0l-.707-.707m12.728 12.728l-.707-.707m-10.607 0l-.707.707M12 5a7 7 0 1 0 7 7" />
      `;
}
}

themeBtn.addEventListener('click', () => {
    document.documentElement.classList.toggle('dark');
    const isDark = document.documentElement.classList.contains('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    updateIcon();
});

// Set icon on initial load
updateIcon();