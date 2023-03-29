import jwt_decode from 'jwt-decode';

export const validateToken = async () => {
    const token = localStorage.getItem('token');

    if (!token) {
        return false;
    }

    try {
        const decoded = jwt_decode(token);
        const currentTime = Date.now() / 1000;

        if (decoded.exp && decoded.exp > currentTime) {
            return true;
        } else {
            localStorage.removeItem('token');
            localStorage.removeItem('refresh');
            return false;
        }
    } catch (error) {
        localStorage.removeItem('token');
        localStorage.removeItem('refresh');
        return false;
    }
};