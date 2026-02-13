import { useEffect, useState } from 'react';
import axios from '../api/axios';

export default function AdminPage() {
  const [mode, setMode] = useState('clients');

  // --- CLIENTS ---
  const [clients, setClients] = useState([]);
  const [clientForm, setClientForm] = useState({
    fullName: '',
    email: '',
    phone: '',
    notes: '',
    role: 'client',
    password: ''
  });
  const [editingClient, setEditingClient] = useState(null);

  const handleCreateClient = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('/clients', clientForm);
      setClients([...clients, res.data]);
      setClientForm({ fullName: '', email: '', phone: '', notes: '', role: 'client', password: '' });
    } catch (err) {
      alert(err.response?.data?.error || 'Ошибка создания клиента');
    }
  };

  const handleDeleteClient = async (id) => {
    try {
      await axios.delete(`/clients/${id}`);
      setClients(clients.filter(c => c._id !== id));
    } catch {
      alert('Ошибка удаления клиента');
    }
  };

  const handleEditClientSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.put(`/clients/${editingClient._id}`, editingClient);
      setClients(clients.map(c => c._id === editingClient._id ? res.data : c));
      setEditingClient(null);
    } catch {
      alert('Ошибка обновления клиента');
    }
  };

  // --- PROCEDURES ---
  const [procedures, setProcedures] = useState([]);
  const [procedureForm, setProcedureForm] = useState({
    name: '',
    category: 'face',
    price: '',
    durationMin: '',
    description: ''
  });
  const [editingProcedure, setEditingProcedure] = useState(null);

  const handleCreateProcedure = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('/procedures', procedureForm);
      setProcedures([...procedures, res.data]);
      setProcedureForm({ name: '', category: 'face', price: '', durationMin: '', description: '' });
    } catch (err) {
      alert(err.response?.data?.error || 'Ошибка создания процедуры');
    }
  };

  const handleDeleteProcedure = async (id) => {
    try {
      await axios.delete(`/procedures/${id}`);
      setProcedures(procedures.filter(p => p._id !== id));
    } catch {
      alert('Ошибка удаления процедуры');
    }
  };

  const handleEditProcedureSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.put(`/procedures/${editingProcedure._id}`, editingProcedure);
      setProcedures(procedures.map(p => p._id === editingProcedure._id ? res.data : p));
      setEditingProcedure(null);
    } catch {
      alert('Ошибка обновления процедуры');
    }
  };

  // --- APPOINTMENTS ---
  const [appointments, setAppointments] = useState([]);
  const [appointmentForm, setAppointmentForm] = useState({
    clientId: '',
    procedureId: '',
    startUtc: '',
    status: 'scheduled',
    notes: ''
  });
  const [editingAppointment, setEditingAppointment] = useState(null);

  const handleCreateAppointment = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('/appointments', appointmentForm);
      setAppointments([...appointments, res.data]);
      setAppointmentForm({ clientId: '', procedureId: '', startUtc: '', status: 'scheduled', notes: '' });
    } catch (err) {
      alert(err.response?.data?.error || 'Ошибка создания записи');
    }
  };

  const handleDeleteAppointment = async (id) => {
    try {
      await axios.delete(`/appointments/${id}`);
      setAppointments(appointments.filter(a => a._id !== id));
    } catch {
      alert('Ошибка удаления записи');
    }
  };

  const handleEditAppointmentSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.put(`/appointments/${editingAppointment._id}`, editingAppointment);
      setAppointments(appointments.map(a => a._id === editingAppointment._id ? res.data : a));
      setEditingAppointment(null);
    } catch {
      alert('Ошибка обновления записи');
    }
  };

  // --- PLANS ---
  const [plans, setPlans] = useState([]);
  const [planForm, setPlanForm] = useState({
    clientId: '',
    title: '',
    procedures: [],
    progress: 0
  });
  const [editingPlan, setEditingPlan] = useState(null);
  const [selectedProcedure, setSelectedProcedure] = useState('');
  const [selectedDate, setSelectedDate] = useState('');

  const handleCreatePlan = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('/plans', planForm);
      setPlans([...plans, res.data]);
      setPlanForm({ clientId: '', title: '', procedures: [], progress: 0 });
    } catch (err) {
      alert(err.response?.data?.error || 'Ошибка создания плана');
    }
  };

  const handleDeletePlan = async (id) => {
    try {
      await axios.delete(`/plans/${id}`);
      setPlans(plans.filter(p => p._id !== id));
    } catch {
      alert('Ошибка удаления плана');
    }
  };

  const handleEditPlanSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.put(`/plans/${editingPlan._id}`, editingPlan);
      setPlans(plans.map(p => p._id === editingPlan._id ? res.data : p));
      setEditingPlan(null);
    } catch {
      alert('Ошибка обновления плана');
    }
  };

  // --- DATA LOADING ---
  useEffect(() => {
    if (mode === 'clients') {
      axios.get('/clients').then(res => setClients(res.data)).catch(err => console.error(err));
    }
    if (mode === 'procedures') {
      axios.get('/procedures').then(res => setProcedures(res.data)).catch(err => console.error(err));
    }
    if (mode === 'appointments') {
      axios.get('/appointments').then(res => setAppointments(res.data)).catch(err => console.error(err));
      axios.get('/clients').then(res => setClients(res.data)).catch(err => console.error(err));
      axios.get('/procedures').then(res => setProcedures(res.data)).catch(err => console.error(err));
    }
    if (mode === 'plans') {
      axios.get('/plans').then(res => setPlans(res.data)).catch(err => console.error(err));
      axios.get('/clients').then(res => setClients(res.data)).catch(err => console.error(err));
      axios.get('/procedures').then(res => setProcedures(res.data)).catch(err => console.error(err));
    }
  }, [mode]);

  return (
    <main className="container section fade-in">
      <article className="card">
        <h2 className="h2">Админ‑панель</h2>

                {/* переключатель */}
        <div className="form__actions btn-group">
          <button
            className={`btn ${mode === 'clients' ? 'btn--success' : 'btn--ghost'}`}
            onClick={() => setMode('clients')}
          >
            👤 Клиенты
          </button>
          <button
            className={`btn ${mode === 'procedures' ? 'btn--success' : 'btn--ghost'}`}
            onClick={() => setMode('procedures')}
          >
            💆 Процедуры
          </button>
          <button
            className={`btn ${mode === 'appointments' ? 'btn--success' : 'btn--ghost'}`}
            onClick={() => setMode('appointments')}
          >
            📅 Записи
          </button>


          <button
            className={`btn ${mode === 'plans' ? 'btn--success' : 'btn--ghost'}`}
            onClick={() => setMode('plans')}
          >
            💻 Курсы
          </button>
        </div>


        {/* блок клиентов */}
        {mode === 'clients' && (
          <>
            <form className="form" onSubmit={handleCreateClient}>
              <input className="form__input" placeholder="ФИО" value={clientForm.fullName}
                     onChange={e => setClientForm({ ...clientForm, fullName: e.target.value })} required />
              <input className="form__input" placeholder="Email" type="email" value={clientForm.email}
                     onChange={e => setClientForm({ ...clientForm, email: e.target.value })} required />
              <input className="form__input" placeholder="Телефон" value={clientForm.phone}
                     onChange={e => setClientForm({ ...clientForm, phone: e.target.value })} required />
              <input className="form__input" placeholder="Пароль" type="password" value={clientForm.password}
                     onChange={e => setClientForm({ ...clientForm, password: e.target.value })} required />
              <textarea className="form__input" placeholder="Заметки" value={clientForm.notes}
                        onChange={e => setClientForm({ ...clientForm, notes: e.target.value })} />
              <select className="form__input" value={clientForm.role}
                      onChange={e => setClientForm({ ...clientForm, role: e.target.value })}>
                <option value="client">Клиент</option>
                <option value="admin">Админ</option>
              </select>
              <div className="form__actions">
                <button className="btn btn--success" type="submit">Добавить клиента</button>
              </div>
            </form>

            <ul className="info-list">
              {clients.map(c => (
                <li key={c._id} className="info-list__item">
                  <div>
                    <strong>{c.fullName}</strong> ({c.role})<br />
                    Email: {c.email}<br />
                    Телефон: {c.phone}<br />
                    Заметки: {c.notes || '—'}
                  </div>
                  <div className="form__actions">
                    <button className="btn btn--ghost" onClick={() => setEditingClient(c)}>Редактировать</button>
                    <button className="btn btn--danger" onClick={() => handleDeleteClient(c._id)}>Удалить</button>
                  </div>
                </li>
              ))}
            </ul>

            {editingClient && (
              <form className="form" onSubmit={handleEditClientSubmit}>
                <h3 className="h2">Редактирование клиента</h3>
                <input className="form__input" name="fullName" value={editingClient.fullName}
                       onChange={e => setEditingClient({ ...editingClient, fullName: e.target.value })} />
                <input className="form__input" name="email" type="email" value={editingClient.email}
                       onChange={e => setEditingClient({ ...editingClient, email: e.target.value })} />
                <input className="form__input" name="phone" value={editingClient.phone}
                       onChange={e => setEditingClient({ ...editingClient, phone: e.target.value })} />
                <textarea className="form__input" name="notes" value={editingClient.notes || ''}
                          onChange={e => setEditingClient({ ...editingClient, notes: e.target.value })} />
                <select className="form__input" name="role" value={editingClient.role}
                        onChange={e => setEditingClient({ ...editingClient, role: e.target.value })}>
                  <option value="client">Клиент</option>
                  <option value="admin">Админ</option>
                </select>
                <div className="form__actions">
                  <button className="btn btn--success" type="submit">Сохранить</button>
                  <button className="btn btn--ghost" type="button" onClick={() => setEditingClient(null)}>Отмена</button>
                </div>
              </form>
            )}
          </>
        )}


{mode === 'appointments' && (
  <>
    {/* форма добавления записи */}
    <form className="form" onSubmit={handleCreateAppointment}>
      <select
        className="form__input"
        value={appointmentForm.clientId}
        onChange={e => setAppointmentForm({ ...appointmentForm, clientId: e.target.value })}
        required
      >
        <option value="">Выберите клиента</option>
        {clients.map(c => (
          <option key={c._id} value={c._id}>
            {c.fullName} ({c.email})
          </option>
        ))}
      </select>

      <select
        className="form__input"
        value={appointmentForm.procedureId}
        onChange={e => setAppointmentForm({ ...appointmentForm, procedureId: e.target.value })}
        required
      >
        <option value="">Выберите процедуру</option>
        {procedures.map(p => (
          <option key={p._id} value={p._id}>
            {p.name}
          </option>
        ))}
      </select>

      <input
        className="form__input"
        type="datetime-local"
        value={appointmentForm.startUtc}
        onChange={e => setAppointmentForm({ ...appointmentForm, startUtc: e.target.value })}
        required
      />

      <select
        className="form__input"
        value={appointmentForm.status}
        onChange={e => setAppointmentForm({ ...appointmentForm, status: e.target.value })}
      >
        <option value="scheduled">Запланировано</option>
        <option value="completed">Завершено</option>
        <option value="canceled">Отменено</option>
      </select>

      <textarea
        className="form__input"
        placeholder="Заметки"
        value={appointmentForm.notes}
        onChange={e => setAppointmentForm({ ...appointmentForm, notes: e.target.value })}
      />

      <button className="btn btn--success" type="submit">Добавить запись</button>
    </form>

    {/* список записей */}
    <ul className="info-list">
      {appointments.map(a => (
        <li key={a._id} className="info-list__item">
          <div>
            Клиент: {a.clientId?.fullName} ({a.clientId?.email})<br />
            Процедура: {a.procedureId?.name}<br />
            Дата: {new Date(a.startUtc).toLocaleString()}<br />
            Статус: {a.status}<br />
            Заметки: {a.notes || '—'}
          </div>
          <div className="form__actions">
            <button className="btn btn--ghost" onClick={() => setEditingAppointment(a)}>Редактировать</button>
            <button className="btn btn--danger" onClick={() => handleDeleteAppointment(a._id)}>Удалить</button>
          </div>
        </li>
      ))}
    </ul>

    {/* форма редактирования */}
    {editingAppointment && (
      <form className="form" onSubmit={handleEditAppointmentSubmit}>
        <h3 className="h2">Редактирование записи</h3>

        <select
          className="form__input"
          name="clientId"
          value={editingAppointment.clientId?._id || editingAppointment.clientId}
          onChange={e => setEditingAppointment({ ...editingAppointment, clientId: e.target.value })}
        >
          {clients.map(c => (
            <option key={c._id} value={c._id}>
              {c.fullName} ({c.email})
            </option>
          ))}
        </select>

        <select
          className="form__input"
          name="procedureId"
          value={editingAppointment.procedureId?._id || editingAppointment.procedureId}
          onChange={e => setEditingAppointment({ ...editingAppointment, procedureId: e.target.value })}
        >
          {procedures.map(p => (
            <option key={p._id} value={p._id}>
              {p.name}
            </option>
          ))}
        </select>

        <input
          className="form__input"
          type="datetime-local"
          name="startUtc"
          value={editingAppointment.startUtc}
          onChange={e => setEditingAppointment({ ...editingAppointment, startUtc: e.target.value })}
        />

        <select
          className="form__input"
          name="status"
          value={editingAppointment.status}
          onChange={e => setEditingAppointment({ ...editingAppointment, status: e.target.value })}
        >
          <option value="scheduled">Запланировано</option>
          <option value="completed">Завершено</option>
          <option value="canceled">Отменено</option>
        </select>

        <textarea
          className="form__input"
          name="notes"
          value={editingAppointment.notes || ''}
          onChange={e => setEditingAppointment({ ...editingAppointment, notes: e.target.value })}
        />

        <div className="form__actions">
          <button className="btn btn--success" type="submit">Сохранить</button>
          <button className="btn btn--ghost" type="button" onClick={() => setEditingAppointment(null)}>Отмена</button>
        </div>
      </form>
    )}
  </>
)}


        

{mode === 'plans' && (
  <>
    {/* форма создания плана */}
    <form className="form" onSubmit={handleCreatePlan}>
      {/* выбор клиента */}
      <select
        className="form__input"
        value={planForm.clientId}
        onChange={e => setPlanForm({ ...planForm, clientId: e.target.value })}
        required
      >
        <option value="">Выберите клиента</option>
        {clients.map(c => (
          <option key={c._id} value={c._id}>
            {c.fullName} ({c.email})
          </option>
        ))}
      </select>

      {/* название плана */}
      <input
        className="form__input"
        placeholder="Название плана"
        value={planForm.title}
        onChange={e => setPlanForm({ ...planForm, title: e.target.value })}
        required
      />

      {/* выбор процедуры + дата + кнопка добавить */}
      <div className="form__actions">
        <select
          className="form__input"
          value={selectedProcedure}
          onChange={e => setSelectedProcedure(e.target.value)}
        >
          <option value="">Выберите процедуру</option>
          {procedures.map(p => (
            <option key={p._id} value={p._id}>
              {p.name}
            </option>
          ))}
        </select>

        <input
          className="form__input"
          type="date"
          value={selectedDate}
          onChange={e => setSelectedDate(e.target.value)}
        />

        <button
          type="button"
          className="btn btn--ghost"
          onClick={() => {
            if (selectedProcedure && selectedDate) {
              setPlanForm({
                ...planForm,
                procedures: [
                  ...planForm.procedures,
                  {
                    procedureId: selectedProcedure,
                    plannedDateUtc: new Date(selectedDate).toISOString(),
                    done: false
                  }
                ]
              });
              setSelectedProcedure('');
              setSelectedDate('');
            }
          }}
        >
          ➕ Добавить процедуру
        </button>
      </div>

      {/* список выбранных процедур */}
      <ul className="info-list">
        {planForm.procedures.map((proc, idx) => {
          const p = procedures.find(pr => pr._id === proc.procedureId);
          return (
            <li key={idx} className="info-list__item">
              {p?.name} — {new Date(proc.plannedDateUtc).toLocaleDateString()}
              <button
                type="button"
                className="btn btn--danger btn--small"
                onClick={() => {
                  setPlanForm({
                    ...planForm,
                    procedures: planForm.procedures.filter((_, i) => i !== idx)
                  });
                }}
              >
                ✖
              </button>
            </li>
          );
        })}
      </ul>

      {/* прогресс */}
      <input
        className="form__input"
        type="number"
        min="0"
        max="100"
        value={planForm.progress}
        onChange={e => setPlanForm({ ...planForm, progress: e.target.value })}
        placeholder="Прогресс (%)"
      />

      <button className="btn btn--success" type="submit">Создать план</button>
    </form>

    {/* список планов */}
    <ul className="info-list">
      {plans.map(p => {
        const client = clients.find(c => c._id === (p.clientId?._id || p.clientId));
        return (
          <li key={p._id} className="info-list__item">
            <div>
              <strong>{p.title}</strong><br />
              Клиент: {client?.fullName} ({client?.email})<br />
              Прогресс: {p.progress}%<br />
              Процедуры:
              <ul>
                {p.procedures.map((proc, idx) => {
                  const pr = procedures.find(pr => pr._id === (proc.procedureId?._id || proc.procedureId));
                  return (
                    <li key={idx}>
                      {pr?.name} — {new Date(proc.plannedDateUtc).toLocaleDateString()} [{proc.done ? '✔' : '✖'}]
                    </li>
                  );
                })}
              </ul>
            </div>
            <div className="form__actions">
              <button className="btn btn--ghost" onClick={() => setEditingPlan(p)}>Редактировать</button>
              <button className="btn btn--danger" onClick={() => handleDeletePlan(p._id)}>Удалить</button>
            </div>
          </li>
        );
      })}
    </ul>

    {/* форма редактирования плана */}
    {editingPlan && (
      <form className="form" onSubmit={handleEditPlanSubmit}>
        <h3 className="h2">Редактирование плана</h3>

        {/* выбор клиента */}
        <select
          className="form__input"
          value={editingPlan.clientId?._id || editingPlan.clientId}
          onChange={e => setEditingPlan({ ...editingPlan, clientId: e.target.value })}
          required
        >
          <option value="">Выберите клиента</option>
          {clients.map(c => (
            <option key={c._id} value={c._id}>
              {c.fullName} ({c.email})
            </option>
          ))}
        </select>

        {/* название плана */}
        <input
          className="form__input"
          name="title"
          value={editingPlan.title}
          onChange={e => setEditingPlan({ ...editingPlan, title: e.target.value })}
        />

        {/* прогресс */}
        <input
          className="form__input"
          type="number"
          min="0"
          max="100"
          name="progress"
          value={editingPlan.progress}
          onChange={e => setEditingPlan({ ...editingPlan, progress: e.target.value })}
        />

        {/* редактирование процедур и дат */}
        <ul className="info-list">
          {editingPlan.procedures.map((proc, idx) => {
            const pr = procedures.find(pr => pr._id === (proc.procedureId?._id || proc.procedureId));
            return (
              <li key={idx} className="info-list__item">
                {pr?.name}
                <input
                  className="form__input"
                  type="date"
                  value={new Date(proc.plannedDateUtc).toISOString().split('T')[0]}
                  onChange={e => {
                    const updated = [...editingPlan.procedures];
                    updated[idx].plannedDateUtc = new Date(e.target.value).toISOString();
                    setEditingPlan({ ...editingPlan, procedures: updated });
                  }}
                />
              </li>
            );
          })}
        </ul>

        <div className="form__actions">
          <button className="btn btn--success" type="submit">Сохранить</button>
          <button className="btn btn--ghost" type="button" onClick={() => setEditingPlan(null)}>Отмена</button>
        </div>
      </form>
    )}
  </>
)}





        {/* блок процедур */}
        {mode === 'procedures' && (
          <>
            <form className="form" onSubmit={handleCreateProcedure}>
              <input className="form__input" placeholder="Название" value={procedureForm.name}
                     onChange={e => setProcedureForm({ ...procedureForm, name: e.target.value })} required />
              <select className="form__input" value={procedureForm.category}
                      onChange={e => setProcedureForm({ ...procedureForm, category: e.target.value })}>
                  <option value="face">Лицо</option>
                  <option value="body">Тело</option>
                  <option value="hair">Волосы</option>
                  <option value="spa">SPA</option>
              </select>
              <input
                className="form__input"
                name="price"
                type="number"
                value={procedureForm.price}
                onChange={e => setProcedureForm({ ...procedureForm, price: e.target.value })}
                placeholder="Цена"
                required
              />
              <input
                className="form__input"
                name="durationMin"
                type="number"
                value={procedureForm.durationMin}
                onChange={e => setProcedureForm({ ...procedureForm, durationMin: e.target.value })}
                placeholder="Длительность (мин)"
                required
              />
              <textarea
                className="form__input"
                name="description"
                value={procedureForm.description}
                onChange={e => setProcedureForm({ ...procedureForm, description: e.target.value })}
                placeholder="Описание"
              />
              <div className="form__actions">
                <button className="btn btn--success" type="submit">Добавить процедуру</button>
              </div>
            </form>

            {/* список процедур */}
            <ul className="info-list">
              {procedures.map(p => (
                <li key={p._id} className="info-list__item">
                  <div>
                    <strong>{p.name}</strong> <span className="muted">({p.category})</span><br />
                    <span className="info-list__label">Цена:</span> {p.price} ₽<br />
                    <span className="info-list__label">Длительность:</span> {p.durationMin} мин<br />
                    <span className="info-list__label">Описание:</span> {p.description || '—'}
                  </div>
                  <div className="form__actions">
                    <button className="btn btn--ghost" onClick={() => setEditingProcedure(p)}>Редактировать</button>
                    <button className="btn btn--danger" onClick={() => handleDeleteProcedure(p._id)}>Удалить</button>
                  </div>
                </li>
              ))}
            </ul>

            {/* форма редактирования процедуры */}
            {editingProcedure && (
              <form className="form" onSubmit={handleEditProcedureSubmit}>
                <h3 className="h2">Редактирование процедуры</h3>
                <input
                  className="form__input"
                  name="name"
                  value={editingProcedure.name}
                  onChange={e => setEditingProcedure({ ...editingProcedure, name: e.target.value })}
                  placeholder="Название"
                  required
                />
                <select
                  className="form__input"
                  name="category"
                  value={editingProcedure.category}
                  onChange={e => setEditingProcedure({ ...editingProcedure, category: e.target.value })}
                >
                  <option value="face">Лицо</option>
                  <option value="body">Тело</option>
                  <option value="hair">Волосы</option>
                  <option value="spa">SPA</option>
                </select>
                <input
                  className="form__input"
                  name="price"
                  type="number"
                  value={editingProcedure.price}
                  onChange={e => setEditingProcedure({ ...editingProcedure, price: e.target.value })}
                  placeholder="Цена"
                  required
                />
                <input
                  className="form__input"
                  name="durationMin"
                  type="number"
                  value={editingProcedure.durationMin}
                  onChange={e => setEditingProcedure({ ...editingProcedure, durationMin: e.target.value })}
                  placeholder="Длительность (мин)"
                  required
                />
                <textarea
                  className="form__input"
                  name="description"
                  value={editingProcedure.description || ''}
                  onChange={e => setEditingProcedure({ ...editingProcedure, description: e.target.value })}
                  placeholder="Описание"
                />
                <div className="form__actions">
                  <button className="btn btn--success" type="submit">Сохранить</button>
                  <button className="btn btn--ghost" type="button" onClick={() => setEditingProcedure(null)}>Отмена</button>
                </div>
              </form>
            )}
          </>
        )}
      </article>
    </main>
  );
}
