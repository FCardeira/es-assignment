import axios from 'axios';
import { PUBLIC_API_URL } from '$env/static/public';

axios.defaults.baseURL = PUBLIC_API_URL;
axios.defaults.headers.common['Content-Type'] = 'application/json';

axios.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export default axios;