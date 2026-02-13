import { useState, useEffect } from 'react';
import { login } from '../api/auth';
import { useNavigate } from 'react-router-dom';

export default function LoginPage() {
  const [form, setForm] = useState({ email: '', password: '' });
  const navigate = useNavigate();

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      const res = await login(form);
      localStorage.setItem('user', JSON.stringify(res.data.user));
      navigate('/');
    } catch (err) {
      alert(err.response?.data?.error || 'Ошибка входа');
    }
  };

  // обработка токена после редиректа от Google
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const token = params.get('token');
    if (token) {
      localStorage.setItem('access_token', token);
      navigate('/');
    }
  }, [navigate]);

  return (
    <main className="container section fade-in">
      <article className="card card--half">
        <h1 className="h1">Вход</h1>
        <form className="form" onSubmit={handleSubmit}>
          <label className="form__label" htmlFor="email">Email</label>
          <input
            className="form__input"
            id="email"
            name="email"
            type="email"
            onChange={handleChange}
            required
          />

          <label className="form__label" htmlFor="password">Пароль</label>
          <input
            className="form__input"
            id="password"
            name="password"
            type="password"
            onChange={handleChange}
            required
          />

          <div className="form__actions">
            <button className="btn" type="submit">Войти</button>
          </div>
        </form>

        <div className="form__actions" style={{ marginTop: '1rem' }}>
          {/* Кнопка входа через Google */}
         <a href="http://localhost:4000/api/auth/google">
  <button className="btn btn--google" type="button">
    Войти через Google
  </button>
</a>

        </div>
      </article>
    </main>
  );
}
