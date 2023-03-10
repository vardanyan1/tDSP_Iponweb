import { useEffect, useState } from 'react';
import './App.css';
import CampaignsPage from './pages/CampaignsPage';
import LoginPage from './pages/LoginPage';

function App() {
    const [isOkay, setIsOkay] = useState(false);

    useEffect(() => {
        if(window.location.href === 'http://localhost:3000/campaigns/') {
            setIsOkay(true);
        }
    }, [window.location.href]);

  return (
    <div className="App">
      { isOkay ? <CampaignsPage /> : <LoginPage /> }
    </div>
  );
}

export default App;
