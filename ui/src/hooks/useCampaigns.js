import { useMutation, useQuery, useQueryClient } from "react-query";
import axios from "../axios-instance";

export const useCampaigns = () => {
    const queryClient = useQueryClient();

    const { isLoading, isError, data: campaigns } = useQuery(
        "campaigns",
        async () => {
            const { data } = await axios.get("/api/campaigns/");
            return data;
        },
        {
            refetchOnWindowFocus: false,
        }
    );

    const removeCampaign = useMutation((id) => axios.delete(`/api/campaigns/${id}/`), {
        onSuccess: () => {
            queryClient.invalidateQueries("campaigns");
        },
    });

    const createCampaign = useMutation(
        (formValues) => axios.post("/api/campaigns/", formValues),
        {
            onSuccess: () => {
                queryClient.invalidateQueries("campaigns");
            },
        }
    );

    const handleCheckboxChange = useMutation(
        (item) => axios.put(`/api/campaigns/${item.id}/`, { ...item, is_active: !item.is_active }),
        {
            onSuccess: ({ data }, variables) => {
                queryClient.setQueryData("campaigns", (oldData) =>
                    oldData.map((campaign) =>
                        campaign.id === variables.id
                            ? { ...campaign, is_active: data.is_active }
                            : campaign
                    )
                );
            },
        }
    );

    return {
        campaigns,
        isLoading,
        isError,
        removeCampaign,
        createCampaign,
        handleCheckboxChange,
    };
};
