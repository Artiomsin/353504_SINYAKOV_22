document.addEventListener('DOMContentLoaded', () => {
  const switcher = document.getElementById('themeSwitcher');
  const label = document.getElementById('themeLabel');

  // Загружаем сохранённую тему
  const savedTheme = localStorage.getItem('theme') || 'light';
  document.body.classList.add(savedTheme + '-theme');
  switcher.checked = savedTheme === 'dark';
  label.textContent = savedTheme === 'dark' ? 'Тёмная тема' : 'Светлая тема';

  // Слушаем переключатель
  switcher.addEventListener('change', () => {
    document.body.classList.remove('light-theme', 'dark-theme');
    const newTheme = switcher.checked ? 'dark' : 'light';
    document.body.classList.add(newTheme + '-theme');
    localStorage.setItem('theme', newTheme);
    label.textContent = newTheme === 'dark' ? 'Тёмная тема' : 'Светлая тема';
  });
});