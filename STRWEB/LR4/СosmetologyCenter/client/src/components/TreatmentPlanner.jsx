import { useState, useEffect, useCallback } from 'react';
import axios from '../api/axios';

const TreatmentPlanner = ({ userId, onTreatmentPlan }) => {
  const [procedures, setProcedures] = useState([]);
  const [plan, setPlan] = useState({ title: '', procedures: [], progress: 0 });
  const [selectedProcedure, setSelectedProcedure] = useState('');
  const [selectedDate, setSelectedDate] = useState('');
  const [userPlans, setUserPlans] = useState([]);

  // --- Загрузка всех доступных процедур ---
  useEffect(() => {
    axios.get('/procedures')
      .then(res => setProcedures(res.data))
      .catch(err => console.error(err));
  }, []);

  // --- Функция расчёта прогресса ---
  const calculateProgress = (procedures) => {
    if (!procedures || procedures.length === 0) return 0;

    const now = new Date();
    const total = procedures.length;
    const done = procedures.filter(p => new Date(p.plannedDateUtc) <= now).length;

    if (done === 0) return 0;
    if (done === total) return 100;

    return Math.floor((done / total) * 100);
  };

  // --- Загрузка курсов пользователя с пересчётом прогресса ---
  const fetchUserPlans = useCallback(async () => {
    if (!userId) return;
    try {
      const res = await axios.get(`/plans/user/${userId}`);
      const plans = res.data;

      const updatedPlans = await Promise.all(plans.map(async plan => {
        const progress = calculateProgress(plan.procedures);

        if (plan.progress !== progress) {
          const updatedPlan = await axios.put(`/plans/${plan._id}`, { ...plan, progress });
          return updatedPlan.data;
        }
        return plan;
      }));

      // Сортировка: сначала незавершённые, потом завершённые
      updatedPlans.sort((a, b) => {
        if (a.progress === 100 && b.progress < 100) return 1;
        if (a.progress < 100 && b.progress === 100) return -1;
        return 0;
      });

      setUserPlans(updatedPlans);
    } catch (err) {
      console.error(err);
    }
  }, [userId]);

  useEffect(() => {
    fetchUserPlans();
  }, [fetchUserPlans]);

  // --- Добавление процедуры в форму курса ---
  const addProcedure = () => {
    if (!selectedProcedure || !selectedDate) return;
    setPlan(prev => ({
      ...prev,
      procedures: [
        ...prev.procedures,
        { procedureId: selectedProcedure, plannedDateUtc: new Date(selectedDate).toISOString(), done: false }
      ]
    }));
    setSelectedProcedure('');
    setSelectedDate('');
  };

  // --- Удаление процедуры из формы ---
  const removeProcedure = (index) => {
    setPlan(prev => ({
      ...prev,
      procedures: prev.procedures.filter((_, i) => i !== index)
    }));
  };

  // --- Создание нового курса ---
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('/plans', { ...plan, clientId: userId });
      onTreatmentPlan && onTreatmentPlan(res.data);
      setPlan({ title: '', procedures: [], progress: 0 });
      alert('План курса успешно создан!');
      fetchUserPlans();
    } catch (err) {
      alert(err.response?.data?.error || 'Ошибка создания плана');
    }
  };

  // --- Удаление курса ---
  const handleDelete = async (id) => {
    if (!window.confirm('Вы уверены, что хотите удалить этот курс?')) return;
    try {
      await axios.delete(`/plans/${id}`);
      setUserPlans(prev => prev.filter(p => p._id !== id));
      alert('Курс успешно удалён!');
    } catch (err) {
      alert(err.response?.data?.error || 'Ошибка при удалении курса');
    }
  };

  return (
    <div className="treatment-planner container fade-in">
      <h2 className="h2">📝 Планирование курса процедур</h2>

      {/* Форма создания курса */}
      <form onSubmit={handleSubmit} className="form card">
        <input
          type="text"
          placeholder="Название курса"
          className="form__input"
          value={plan.title}
          onChange={e => setPlan({ ...plan, title: e.target.value })}
          required
        />

        <div className="form__actions">
          <select
            value={selectedProcedure}
            onChange={e => setSelectedProcedure(e.target.value)}
            className="form__input"
          >
            <option value="">Выберите процедуру</option>
            {procedures.map(p => (
              <option key={p._id} value={p._id}>{p.name}</option>
            ))}
          </select>

          <input
            type="date"
            value={selectedDate}
            onChange={e => setSelectedDate(e.target.value)}
            className="form__input"
          />

          <button type="button" className="btn" onClick={addProcedure}>➕ Добавить</button>
        </div>

        {/* Список процедур */}
        <ul className="info-list">
          {plan.procedures.map((proc, idx) => {
            const p = procedures.find(pr => pr._id === proc.procedureId);
            return (
              <li key={idx} className="info-list__item future">
                {p?.name} — {new Date(proc.plannedDateUtc).toLocaleDateString()}
                <button type="button" className="btn btn--danger" onClick={() => removeProcedure(idx)}>✖</button>
              </li>
            );
          })}
        </ul>

        <button type="submit" className="btn btn--success">Создать курс</button>
      </form>

      {/* Список всех курсов пользователя */}
      <div className="card">
        <h3 className="h2">Ваши курсы</h3>
        {userPlans.length === 0 ? (
          <p>Курсы пока не созданы.</p>
        ) : (
          <table className="styled-table">
            <thead>
              <tr>
                <th>Название курса</th>
                <th>Процедуры</th>
                <th>Прогресс</th>
                <th>Действия</th>
              </tr>
            </thead>
            <tbody>
              {userPlans.map(plan => (
                <tr key={plan._id}>
                  <td>{plan.title}</td>
                  <td>
                    {plan.procedures.map(p => {
                      const proc = procedures.find(pr => pr._id === p.procedureId);
                      return (
                        <div key={p.procedureId}>
                          {proc?.name} — {new Date(p.plannedDateUtc).toLocaleDateString()} {p.done ? '✅' : ''}
                        </div>
                      );
                    })}
                  </td>
                  <td>{plan.progress}%</td>
                  <td>
                    {plan.progress === 100 ? (
                      <span style={{ color: 'green', fontWeight: '600' }}>Завершён</span>
                    ) : (
                      <button className="btn btn--danger" onClick={() => handleDelete(plan._id)}>Удалить</button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
};

export default TreatmentPlanner;
