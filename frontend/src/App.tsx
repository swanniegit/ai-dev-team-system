import { Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Agents from './pages/Agents'
import Issues from './pages/Issues'
import Wellness from './pages/Wellness'
import Events from './pages/Events'
import Settings from './pages/Settings'

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/agents" element={<Agents />} />
        <Route path="/issues" element={<Issues />} />
        <Route path="/wellness" element={<Wellness />} />
        <Route path="/events" element={<Events />} />
        <Route path="/settings" element={<Settings />} />
      </Routes>
    </Layout>
  )
}

export default App 