import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:4000/api',
  withCredentials: true
});

instance.interceptors.response.use(
  res => res,
  async err => {
    const original = err.config;

    if (!err.response || original._retry) {
      return Promise.reject(err);
    }

    // если access_token истёк → пробуем обновить
    if (err.response.status === 401) {
      // не пытаемся обновить сам запрос /auth/refresh
      if (original.url.includes('/auth/refresh')) {
        window.location.href = '/login';
        return Promise.reject(err);
      }

      original._retry = true;
      try {
        await instance.post('/auth/refresh');
        return instance(original); // повторяем исходный запрос
      } catch (refreshErr) {
        // если обновить не удалось → редиректим
        window.location.href = '/login';
        return Promise.reject(refreshErr);
      }
    }

    return Promise.reject(err);
  }
);

export default instance;
