import axios from 'axios';
import router from '@/router'; // Import router from your project

// Create an instance of axios
const apiClient = axios.create({
  baseURL: 'https://halopst.web.bps.go.id/backend/api/',
  // baseURL: 'http://localhost:8000/api/',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a request interceptor to include the token in every request
apiClient.interceptors.request.use(
  (config) => {
      const token = localStorage.getItem('id_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add a response interceptor to handle errors
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Check if the error response exists and has a response status
    if (error.response) {
      const { status, data } = error.response;
      if (status == 500) {
        // Clear token from localStorage
        localStorage.removeItem('id_token');
        localStorage.removeItem('user');
        localStorage.removeItem('loggedIn');
        localStorage.clear()
        // Redirect to login page
        router.push({ name: 'login' });
      } else if (status == 401) {
        // Clear token from localStorage
        localStorage.removeItem('id_token');
        localStorage.removeItem('user');
        localStorage.removeItem('loggedIn');
        localStorage.clear()
        // Redirect to login page
        router.push({ name: 'login' });
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;
