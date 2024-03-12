import axios from "axios";

console.log(import.meta.env.VITE_API_URL);

export const axiosBase = axios.create({
  baseURL: "http://localhost/api/v1/",
  headers: {
    "user-init-data": 'user={"id":0}',
  },
});
