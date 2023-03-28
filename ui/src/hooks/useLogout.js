import { useNavigate } from "react-router-dom";
import { useMutation } from "react-query";
import axios from "../axios-instance";

export const useLogout = () => {
  const navigate = useNavigate();

  const logoutMutation = useMutation(() => {
    axios.post("/api/logout/", {refresh_token: localStorage.getItem("refresh")}, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    }).then(() => {
        localStorage.removeItem("token");
        localStorage.removeItem("refresh");
        navigate("/ui/");
    })
    }
  );

  return {
    handleLogout: logoutMutation.mutate,
    isLoading: logoutMutation.isLoading,
    isError: logoutMutation.isError,
  };
};
