import { useEffect, useState } from "react";
import axios from "../axios-instance";

export const useFetchGetData = (url, setData) => {
    const [isLoading, setIsLoading] = useState(true);
    const [isError, setIsError] = useState(null);

    useEffect(() => {
        (async () => {
            try {
                setIsError(null);
                const result = await axios.get(url);
                setData(result.data);
            } catch (e) {
                setIsLoading(false);
                setIsError(e.message);
            } finally {
                setIsLoading(false);
            }
        })()
    }, [url, setData])

    return {
        isLoading,
        isError
    }
}