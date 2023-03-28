import { useMutation, useQuery, useQueryClient } from "react-query";
import axios from "../axios-instance";

export const useCreatives = () => {
    const queryClient = useQueryClient();

    const { isLoading, isError, data: creatives } = useQuery(
        "creatives",
        async () => {
            const { data } = await axios.get("/api/creatives/");
            return data;
        },
        {
            refetchOnWindowFocus: false,
        }
    );

    const removeCreative = useMutation((id) => axios.delete(`/api/creatives/${id}/`), {
        onSuccess: () => {
            queryClient.invalidateQueries("creatives");
        },
    });

    const createCreative = useMutation(
        (formValues) => {
            const formattedCategories = formValues.categories
                .trim()
                .split(" ")
                .map((category) => ({ code: category }));
            const item = { ...formValues, categories: formattedCategories };
            return axios.post("/api/creatives/", item);
        },
        {
            onSuccess: () => {
                queryClient.invalidateQueries("creatives");
            },
        }
    );

    return {
        creatives,
        isLoading,
        isError,
        removeCreative,
        createCreative,
    };
};
