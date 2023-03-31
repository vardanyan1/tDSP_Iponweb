import jwt_decode from 'jwt-decode';
import { useQuery } from 'react-query';
import { useNavigate } from "react-router-dom";
import axios from '../axios-instance';

export const useTokenValidation = () => {
    const navigate = useNavigate();
    const { isLoading, isError, data: isValid } = useQuery(
        'tokenValidation',
        async () => {
            const token = localStorage.getItem('token');

            if (!token) {
                navigate('/ui/');
                return;
            }

            try {
                const decoded = jwt_decode(token);
                const currentTime = Date.now() / 1000;

                if (decoded.exp && decoded.exp > currentTime) {
                    return true;
                } else {
                    const newToken = await refreshToken();
                    localStorage.setItem('token', newToken);
                    return true;
                }
            } catch (error) {
                localStorage.removeItem('token');
                throw new Error('Invalid token');
            }
        },
        {
            refetchOnWindowFocus: false,
            retry: 1,
            refetchInterval: 15 * 60 * 1000, // Set the refetch interval to 15 minutes
        }
    );

    return {
        isValid,
        isLoading,
        isError,
    };
};

const refreshToken = async () => {
    const refreshToken = localStorage.getItem('refresh');

    if (!refreshToken) {
        throw new Error('Refresh token not found');
    }

    try {
        const { data } = await axios.post('/api/token/refresh/', { refresh: refreshToken });
        return data.access;
    } catch (error) {
        localStorage.removeItem('token');
        localStorage.removeItem('refresh');
        throw new Error('Unable to refresh token');
    }
};
