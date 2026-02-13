import { useState } from 'react';
import { register } from '../api/auth';
import { useNavigate } from 'react-router-dom';

export default function RegisterPage() {
  const [form, setForm] = useState({ fullName: '', email: '', phone: '', password: '' });
  const navigate = useNavigate();

  const handleChange = e => setForm({ ...form, [e.target.name]: e.target.value });
  const handleSubmit = async e => {
    e.preventDefault();
    try {
      const res = await register(form);
      localStorage.setItem('user', JSON.stringify(res.data.user)); // сохраняем весь объект
      navigate('/');
    } catch (err) {
      alert(err.response?.data?.error || 'Ошибка регистрации');
    }
  };

  return (
    <main className="container section fade-in">
      <article className="card card--half">
        <h1 className="h1">Регистрация</h1>
        <form className="form" onSubmit={handleSubmit}>
          <div className="form__row form__row--two">
            <div>
              <label className="form__label" htmlFor="fullName">ФИО</label>
              <input className="form__input" id="fullName" name="fullName" onChange={handleChange} required />
            </div>
            <div>
              <label className="form__label" htmlFor="phone">Телефон</label>
              <input className="form__input" id="phone" name="phone" onChange={handleChange} required />
            </div>
          </div>

          <label className="form__label" htmlFor="email">Email</label>
          <input className="form__input" id="email" name="email" type="email" onChange={handleChange} required />

          <label className="form__label" htmlFor="password">Пароль</label>
          <input className="form__input" id="password" name="password" type="password" onChange={handleChange} required />

          <div className="form__actions">
            <button className="btn" type="submit">Зарегистрироваться</button>
          </div>
        </form>
      </article>
    </main>
  );
}
