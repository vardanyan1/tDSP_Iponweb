import React, {useEffect, useState} from "react";
import axios from 'axios';
import '../styles/campaign.css';

const CampaignsPage = () => {
    const [campaigns, setCampaigns] = useState([]);
    useEffect(() => {
        axios.get('http://localhost:8000/api/campaigns')
            .then(response => {
                setCampaigns(response.data);
            })
    }, []);

    return (
        <div>
            <table>
                <tbody>
                <tr>
                <th>id</th>
                <th>name</th>
                <th>budget</th>
                <th>action</th>
                </tr>
                    {campaigns.map(item => {
                        return (
                            <tr key={item.id}>
                                <td>{item.id}</td>
                                <td>{item.name}</td>
                                <td>{item.budget}</td>
                                <td>
                                    <button>Edit</button>
                                    <button>Delete</button>
                                </td>
                            </tr>
                        );
                    })}
                </tbody>
            </table>
        </div>
    );
};

export default CampaignsPage;
