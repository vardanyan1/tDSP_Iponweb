import axios from "axios";

const instance = axios.create({
    baseURL: "http://localhost:80",
});

instance.interceptors.request.use(
    (config) => {
        const access_token = localStorage.getItem("token");
        if (access_token) {
            config.headers.Authorization = `Bearer ${access_token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

export default instance;