import { Link } from 'react-router-dom';
import { logout } from '../api/auth';

export default function Navbar() {
  const handleLogout = async () => {
    await logout();
    localStorage.removeItem('user'); // очищаем весь объект
    window.location.href = '/login';
  };

  return (
    <header className="navbar">
      <div className="container navbar__inner">
        <div className="navbar__brand">Косметология</div>
        <nav className="navbar__links">
          <Link className="navbar__link" to="/">Главная</Link>
          <Link className="navbar__link" to="/register">Регистрация</Link>
          <Link className="navbar__link" to="/admin">Админ</Link>
          <Link className="navbar__link" to="/timezones">Таймзоны</Link>
          <button className="navbar__btn" onClick={handleLogout}>Выйти</button>
        </nav>
      </div>
    </header>
  );
}
