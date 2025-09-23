
// Dark mode toggle for both desktop and mobile
const themeBtn = document.getElementById('toggle-theme');
const themeBtnMobile = document.getElementById('toggle-theme-mobile');
const themeIcon = document.getElementById('theme-icon');
const themeIconMobile = document.getElementById('theme-icon-mobile');

function updateIcons() {
    if (document.documentElement.classList.contains('dark')) {
        themeIcon.innerHTML =  `
            <path d="M12 3v1m0 16v1m8.485-8.485h-1m-14.97 0h-1m12.728-7.071l-.707.707m-10.607 0l-.707-.707m12.728 12.728l-.707-.707m-10.607 0l-.707.707M12 5a7 7 0 1 0 7 7"></path>
        `;
        themeIconMobile.innerHTML = themeIcon.innerHTML;
    } else {
        themeIcon.innerHTML = `
        <path fill="currentColor" d="M12 3v1m0 16v1m8.485-8.485h-1m-14.97 0h-1m12.728-7.071l-.707.707m-10.607 0l-.707-.707m12.728 12.728l-.707-.707m-10.607 0l-.707.707M12 5a7 7 0 1 0 7 7" />
      `;
        themeIconMobile.innerHTML = themeIcon.innerHTML;
    }
}

function toggleTheme() {
    document.documentElement.classList.toggle('dark');
    localStorage.setItem('theme', document.documentElement.classList.contains('dark') ? 'dark' : 'light');
    updateIcons();
}

themeBtn.addEventListener('click', toggleTheme);
themeBtnMobile.addEventListener('click', toggleTheme);

if (localStorage.getItem('theme') === 'dark') {
    document.documentElement.classList.add('dark');
}
updateIcons();