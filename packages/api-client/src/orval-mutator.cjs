const axios = require('axios');

const AXIOS_INSTANCE = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
});

function setAuthToken(token) {
  if (token) {
    AXIOS_INSTANCE.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete AXIOS_INSTANCE.defaults.headers.common['Authorization'];
  }
}

function customInstance(config, options) {
  return AXIOS_INSTANCE({ ...config, ...options }).then(({ data }) => data);
}

module.exports = {
  AXIOS_INSTANCE,
  setAuthToken,
  customInstance,
};
