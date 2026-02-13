import axios from './axios';

export const register = data => axios.post('/auth/register', data);
export const login = data => axios.post('/auth/login', data);
export const logout = () => axios.post('/auth/logout');
export const getProfile = () => axios.get('/clients/me');