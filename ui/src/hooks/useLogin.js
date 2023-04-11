import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useMutation } from "react-query";
import axios from "../axios-instance";

export const useLogin = () => {
    const navigate = useNavigate();
    const [error, setError] = useState(false);

    const loginMutation = useMutation(
        (loginData) => axios.post("/api/token/", loginData),
        {
            onSuccess: (data) => {
                localStorage.setItem("token", data.data.access);
                localStorage.setItem("refresh", data.data.refresh);
                navigate("/ui/campaigns");
            },
            onError: () => {
                setError(true);
            },
        }
    );

    const handleLogin = (loginData) => {
        loginMutation.mutate(loginData);
    };

    return { handleLogin, error, isLoading: loginMutation.isLoading };
};
