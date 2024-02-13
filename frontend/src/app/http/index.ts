import axios from "axios";

export const axiosUser = axios.create({
    baseURL: 'http://localhost:8000/users'
})


export const axiosProjects = axios.create({
    baseURL: 'http://localhost:8000/projects'
})