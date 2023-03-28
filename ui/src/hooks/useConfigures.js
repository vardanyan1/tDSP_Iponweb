import { useQuery } from "react-query";
import axios from "../axios-instance";

export const useConfigures = () => {
    const { isLoading, isError, data: configures } = useQuery(
        "configures",
        async () => {
            const { data } = await axios.get("/game/configure/");
            return data[0];
        },
        {
            refetchOnWindowFocus: false,
        }
    );

    const formatDate = (dateString) => {
        if (dateString) {
            const date = new Date(dateString);

            const day = String(date.getDate()).padStart(2, "0");
            const month = String(date.getMonth() + 1).padStart(2, "0");
            const year = date.getFullYear();

            const hours = String(date.getHours()).padStart(2, "0");
            const minutes = String(date.getMinutes()).padStart(2, "0");

            return `${day}/${month}/${year} ${hours}:${minutes}`;
        }
    };

    const configItems = [
        { label: "Id", value: configures?.id },
        { label: "Mode", value: configures?.mode },
        { label: "Auction type", value: configures?.auction_type },
        { label: "Game goal", value: configures?.game_goal },
        {
            label: "Current",
            value: configures?.current ? "true" : "",
        },
        { label: "Budget", value: configures?.budget },
        { label: "Rounds left", value: configures?.rounds_left },
        { label: "Frequency capping", value: configures?.frequency_capping },
        { label: "Click revenue", value: configures?.click_revenue },
        { label: "Conversion revenue", value: configures?.conversion_revenue },
        { label: "Impression revenue", value: configures?.impression_revenue },
        { label: "Impressions total", value: configures?.impressions_total },
        {
            label: "Created at",
            value: formatDate(configures?.created_at),
        },
    ];

    return {
        isLoading,
        isError,
        configItems
    };
};
