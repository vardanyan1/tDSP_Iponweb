import React, { useEffect, useState } from "react";
import axios from "axios";
import "../styles/campaign.css";
import TableItems from "../components/TableItems";
import CreateCampaignItemModal from "../components/CreateCampaignItemModal";

const CampaignsPage = () => {
  const [campaigns, setCampaigns] = useState([
    { id: 1, name: "sonik", budget: 50000 },
    { id: 2, name: "panaSoniK", budget: 100000 },
    { id: 3, name: "traraSoniK", budget: 10 },
  ]);
  const [isOpenModal, setIsOpenModal] = useState(false);

  useEffect(() => {
    axios.get("http://localhost:8000/api/campaigns").then((response) => {
      setCampaigns(response.data);
    });
  }, []);

  const handleEdit = (id) => {};
  const handleRemove = (id) => {};

  const handleCreateCampaignItem = () => {
    setIsOpenModal(!isOpenModal);
  };

  const handleCloseModal = () => {
    setIsOpenModal(!isOpenModal);
  };
  console.log(isOpenModal);
  return (
    <div className="tableWrapper">
      <div className="container">
        <div className="row justify-content-center">
          <div className="col-md-6 text-center mb-3">
            <h2 className="heading-section">Campaigns</h2>
          </div>
        </div>
        <div className="createCampaignWrapper">
          <button onClick={handleCreateCampaignItem} className="createCampaign">
            Create
          </button>
        </div>
        <div className="row">
          <div className="col-md-12">
            <div className="table-wrap">
              <table className="table table-bordered table-dark table-hover">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Budget</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {campaigns.map((item) => {
                    return (
                      <TableItems
                        key={item.id}
                        item={item}
                        handleEdit={handleEdit}
                        handleRemove={handleRemove}
                      />
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      {isOpenModal && (
        <CreateCampaignItemModal handleCloseModal={handleCloseModal} />
      )}
    </div>
  );
};

export default CampaignsPage;
