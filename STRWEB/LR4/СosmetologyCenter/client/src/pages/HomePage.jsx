import { useEffect, useState } from 'react';
import { getProfile } from '../api/auth';
import axios from '../api/axios';
import NextAppointmentTimer from '../components/NextAppointmentTimer';
import ProcedureCard from '../components/ProcedureCard';
import SkinAnalyzer from '../components/SkinAnalyzer';
import TreatmentPlanner from '../components/TreatmentPlanner';

export default function HomePage() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [procedures, setProcedures] = useState([]);
  const [futureAppointments, setFutureAppointments] = useState([]);
  const [pastAppointments, setPastAppointments] = useState([]);
  const [sortProc, setSortProc] = useState('priceAsc');
  const [searchProc, setSearchProc] = useState('');
  const [sortApp, setSortApp] = useState('timeAsc');
  const [searchApp, setSearchApp] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [showSkinAnalyzer, setShowSkinAnalyzer] = useState(false);
  const [formData, setFormData] = useState({
    procedureId: '',
    startUtc: '',
    notes: ''
  });

  // Загрузка профиля и процедур
  useEffect(() => {
    getProfile()
      .then(res => setUser(res.data))
      .catch(() => setUser(null))
      .finally(() => setLoading(false));

    axios.get('/procedures')
      .then(res => setProcedures(res.data))
      .catch(err => console.error('Ошибка загрузки процедур:', err));
  }, []);

  // Загрузка записей
  const loadAppointments = () => {
    axios.get('/appointments/')
      .then(r => {
        const now = new Date();
        const future = r.data.filter(a => new Date(a.startUtc) > now);
        const past = r.data.filter(a => new Date(a.startUtc) <= now);
        setFutureAppointments(future);
        setPastAppointments(past);
      })
      .catch(err => console.error('Ошибка загрузки записей:', err));
  };

  useEffect(() => {
    if (user) loadAppointments();
  }, [user]);

  // Создание новой записи
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post('/appointments', { ...formData, clientId: user._id });
      alert('Запись успешно создана!');
      setShowForm(false);
      setShowSkinAnalyzer(false);
      setFormData({ procedureId: '', startUtc: '', notes: '' });
      loadAppointments();
    } catch (err) {
      console.error(err);
      alert('Ошибка при создании записи');
    }
  };

  // --- Сортировка и поиск процедур ---
  const filteredProcedures = procedures
    .filter(p => p.name.toLowerCase().includes(searchProc.toLowerCase()))
    .sort((a, b) => {
      if (sortProc === 'priceAsc') return a.price - b.price;
      if (sortProc === 'priceDesc') return b.price - a.price;
      if (sortProc === 'timeAsc') return a.durationMin - b.durationMin;
      if (sortProc === 'timeDesc') return b.durationMin - a.durationMin;
      return 0;
    });

  // --- Сортировка и поиск записей ---
  const filteredFuture = futureAppointments
    .filter(a => a.procedureId?.name.toLowerCase().includes(searchApp.toLowerCase()))
    .sort((a, b) => {
      if (sortApp === 'timeAsc') return new Date(a.startUtc) - new Date(b.startUtc);
      if (sortApp === 'timeDesc') return new Date(b.startUtc) - new Date(a.startUtc);
      if (sortApp === 'priceAsc') return a.procedureId?.price - b.procedureId?.price;
      if (sortApp === 'priceDesc') return b.procedureId?.price - a.procedureId?.price;
      return 0;
    });

  const filteredPast = pastAppointments
    .filter(a => a.procedureId?.name.toLowerCase().includes(searchApp.toLowerCase()))
    .sort((a, b) => new Date(b.startUtc) - new Date(a.startUtc));

  return (
    <main className="container section fade-in">
      <h1 className="h1">Добро пожаловать!</h1>

      <div className="grid">

        {/* ПРОФИЛЬ */}
        <article className="card card--half">
          <h2 className="h2">Профиль</h2>
          {loading ? (
            <p className="muted">Загрузка...</p>
          ) : !user ? (
            <p className="muted">Войдите или зарегистрируйтесь</p>
          ) : (
            <div className="info-list">
              <div className="info-list__item"><span className="info-list__label">ФИО</span><span>{user.fullName}</span></div>
              <div className="info-list__item"><span className="info-list__label">Email</span><span>{user.email}</span></div>
              <div className="info-list__item"><span className="info-list__label">Роль</span><span>{user.role}</span></div>
            </div>
          )}
        </article>

        {/* НАЗНАЧЕНИЕ КУРСА */}
        {user && (
          <article className="card card--full">
            <h2 className="h2">Назначение курса процедур</h2>
            <TreatmentPlanner
              userId={user._id}
              onTreatmentPlan={plan => alert(`Курс "${plan.title}" успешно создан!`)}
            />
          </article>
        )}

        {/* ФОРМА ЗАПИСИ */}
        {user && (
          <article className="card card--half">
            <h2 className="h2">Запись</h2>
            {!showForm ? (
              <button className="btn" onClick={() => setShowForm(true)}>Записаться</button>
            ) : (
              <form className="form" onSubmit={handleSubmit}>
                <label className="form__label">Процедура</label>
                <select
                  className="form__input"
                  value={formData.procedureId}
                  onChange={e => setFormData({ ...formData, procedureId: e.target.value })}
                  required
                >
                  <option value="">Выберите процедуру</option>
                  {procedures.map(p => (
                    <option key={p._id} value={p._id}>{p.name} — {p.price} ₽</option>
                  ))}
                </select>

                <label className="form__label">Дата и время</label>
                <input
                  type="datetime-local"
                  className="form__input"
                  value={formData.startUtc}
                  onChange={e => setFormData({ ...formData, startUtc: e.target.value })}
                  required
                />

                <label className="form__label">Заметки</label>
                <textarea
                  className="form__input"
                  value={formData.notes}
                  onChange={e => setFormData({ ...formData, notes: e.target.value })}
                />

                <div className="form__actions">
                  <button type="submit" className="btn btn--success">Сохранить</button>
                  <button type="button" className="btn btn--ghost" onClick={() => { setShowForm(false); setShowSkinAnalyzer(false); }}>Отмена</button>
                  <button type="button" className="btn btn--info" onClick={() => setShowSkinAnalyzer(prev => !prev)}>
                    {showSkinAnalyzer ? 'Скрыть консультацию' : 'Консультация'}
                  </button>
                </div>

                {showSkinAnalyzer && (
                  <div className="skin-analyzer-section">
                    <h3 className="h3">Анализ кожи</h3>
                    <SkinAnalyzer />
                  </div>
                )}
              </form>
            )}
          </article>
        )}

        {/* ПРОЦЕДУРЫ */}
        <article className="card card--full">
          <h2 className="h2">Доступные процедуры</h2>
          <div className="form__actions">
            <input
              type="text"
              placeholder="Поиск процедуры..."
              value={searchProc}
              onChange={e => setSearchProc(e.target.value)}
            />
            <select value={sortProc} onChange={e => setSortProc(e.target.value)}>
              <option value="priceAsc">Цена ↑</option>
              <option value="priceDesc">Цена ↓</option>
              <option value="timeAsc">Длительность ↑</option>
              <option value="timeDesc">Длительность ↓</option>
            </select>
          </div>
          {filteredProcedures.length === 0 ? (
            <p className="muted">Нет доступных процедур</p>
          ) : (
            <div className="grid">
              {filteredProcedures.map(p => (
                <ProcedureCard
                  key={p._id}
                  name={p.name}
                  price={p.price}
                  durationMin={p.durationMin}
                />
              ))}
            </div>
          )}
        </article>

        {/* ЗАПИСИ */}
        {user && (
          <article className="card card--full">
            <h2 className="h2">Мои записи</h2>

            {filteredFuture.length > 0 && (
              <NextAppointmentTimer nextDate={filteredFuture[0].startUtc} />
            )}

            <div className="form__actions">
              <input
                type="text"
                placeholder="Поиск по процедуре..."
                value={searchApp}
                onChange={e => setSearchApp(e.target.value)}
              />
              <select value={sortApp} onChange={e => setSortApp(e.target.value)}>
                <option value="timeAsc">Время ↑</option>
                <option value="timeDesc">Время ↓</option>
                <option value="priceAsc">Цена ↑</option>
                <option value="priceDesc">Цена ↓</option>
              </select>
            </div>

            <h3 className="h3">Запланированные</h3>
            {filteredFuture.length === 0 ? (
              <p className="muted">Нет запланированных записей</p>
            ) : (
              <ul className="info-list">
                {filteredFuture.map(a => (
                  <li key={a._id} className="info-list__item future">
                    <div><strong>Процедура:</strong> {a.procedureId?.name}</div>
                    <div><strong>Цена:</strong> {a.procedureId?.price} ₽</div>
                    <div><strong>Дата:</strong> {new Date(a.startUtc).toLocaleString()}</div>
                    <div><strong>Статус:</strong> {a.status}</div>
                  </li>
                ))}
              </ul>
            )}

            <h3 className="h3">Завершённые</h3>
            {filteredPast.length === 0 ? (
              <p className="muted">Нет завершённых записей</p>
            ) : (
              <ul className="info-list">
                {filteredPast.map(a => (
                  <li key={a._id} className="info-list__item past">
                    <div><strong>Процедура:</strong> {a.procedureId?.name}</div>
                    <div><strong>Цена:</strong> {a.procedureId?.price} ₽</div>
                    <div><strong>Дата:</strong> {new Date(a.startUtc).toLocaleString()}</div>
                    <div><strong>Статус:</strong> {a.status}</div>
                  </li>
                ))}
              </ul>
            )}
          </article>
        )}

      </div>
    </main>
  );
}
