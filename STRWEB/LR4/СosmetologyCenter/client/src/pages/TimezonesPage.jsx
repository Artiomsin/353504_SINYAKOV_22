import { useEffect, useState } from 'react';
import axios from '../api/axios';

export default function TimezonesPage() {
  const [appointments, setAppointments] = useState([]);

  useEffect(() => {
    axios.get('/appointments')
      .then(res => setAppointments(res.data))
      .catch(err => console.error('Ошибка загрузки:', err));
  }, []);

  const now = new Date();

  return (
    <main className="container section fade-in">
      <h1 className="h1">Таймзоны и даты</h1>
      <p>Текущее локальное время: {now.toLocaleString()}</p>
      <p>Текущее UTC: {now.toISOString()}</p>

      <article className="card card--full">
        <h2 className="h2">Записи</h2>
        {appointments.length === 0 ? (
          <p className="muted">Нет записей</p>
        ) : (
          <table className="styled-table">
            <thead>
              <tr>
                <th>Процедура</th>
                <th>Локальное время</th>
                <th>UTC</th>
                <th>Добавлено</th>
                <th>Изменено</th>
              </tr>
            </thead>
            <tbody>
              {appointments.map(a => (
                <tr key={a._id}>
                  <td>{a.procedureId?.name}</td>
                  <td>{new Date(a.startUtc).toLocaleString()}</td>
                  <td>{new Date(a.startUtc).toISOString()}</td>
                  <td>{new Date(a.createdAt).toLocaleString()}</td>
                  <td>{new Date(a.updatedAt).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </article>
    </main>
  );
}
