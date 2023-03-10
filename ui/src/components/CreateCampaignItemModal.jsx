import React from "react";
import "../styles/campaignItemModal.css";

const CreateCampaignItemModal = ({ handleCloseModal }) => {
  return (
    <div>
      <div id="modal" className="modal">
        <div className="modal-content">
          <h2>Create a new item</h2>
          <form>
            <label htmlFor="input1">Input 1:</label>
            <input type="text" id="input1" name="input1" />

            <label htmlFor="input2">Input 2:</label>
            <input type="text" id="input2" name="input2" />

            <label htmlFor="input3">Input 3:</label>
            <input type="text" id="input3" name="input3" />

            <div className="campaignModalBtnWrapper">
              <button className="saveCampaignItem" id="save-btn" type="submit">
                Save
              </button>
              <button
                className="closeCampaignItemModal"
                onClick={handleCloseModal}
                id="close-btn"
                type="button"
              >
                Close
              </button>
            </div>
          </form>
        </div>
      </div>

      <div id="overlay"></div>
    </div>
  );
};

export default CreateCampaignItemModal;
