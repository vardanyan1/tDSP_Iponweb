import { useEffect, useState } from "react";
import axios from "../axios-instance";
import { useNavigate } from "react-router-dom";

export const useFetchGetData = (url, setData) => {
    const [isLoading, setIsLoading] = useState(true);
    const [isError, setIsError] = useState(null);
    const navigate = useNavigate();

    useEffect(() => {
        const access_token = localStorage.getItem("token");

        if (!access_token) {
            navigate("/ui/");
        } else {
            setIsLoading(true);
            setIsError(null);

            axios
                .get(url, { headers: { Authorization: `Bearer ${access_token}` } })
                .then((response) => {
                    if (url !== "/game/configure/") {
                        setData(response.data);
                        return;
                    }

                    setData(response.data[0]);
                })
                .catch((error) => {
                    setIsError(error.message);
                })
                .finally(() => {
                    setIsLoading(false);
                });
        }
    }, [url, setData, navigate]);

    return {
        isLoading,
        isError,
    };
};