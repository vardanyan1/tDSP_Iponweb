import LoginPage from './pages/LoginPage';
import CampaignsPage from './pages/CampaignsPage';
import CreativesPage from './pages/CreativesPage';
import ConfiguresPage from './pages/ConfiguresPage';

const routes = [
    {
        path: "/ui",
        element: <LoginPage />,
        isPrivate: false,
    },
    {
        path: "/ui/campaigns",
        element: <CampaignsPage />,
        isPrivate: true,
    },
    {
        path: "/ui/creatives",
        element: <CreativesPage />,
        isPrivate: true,
    },
    {
        path: "/ui/configure",
        element: <ConfiguresPage />,
        isPrivate: true,
    },
];

export default routes;
