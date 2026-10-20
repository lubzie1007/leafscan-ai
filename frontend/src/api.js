import axios from 'axios';

// This will use '/api' locally (which proxies to 127.0.0.1:8000).
// If you deploy later, you can add VITE_API_URL back to your hosting platform.
const API_URL = import.meta.env.VITE_API_URL || '/api';

const client = axios.create({
  baseURL: API_URL,
  timeout: 60000,
});

export async function predictLeaf(file) {
  const formData = new FormData();
  formData.append('file', file);

  const response = await client.post('/predict', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  });

  return response.data;
}

export async function healthCheck() {
  const response = await client.get('/health');
  return response.data;
}