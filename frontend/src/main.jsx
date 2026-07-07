import { StrictMode } from 'react'

import { createRoot } from 'react-dom/client'

import { BrowserRouter, Routes, Route } from 'react-router-dom'

import './index.css'

import App from './App.jsx'

import Landing from './components/Landing.jsx'

import AuthCallback from './components/AuthCallback.jsx'

import ProtectedRoute from './components/ProtectedRoute.jsx'



createRoot(document.getElementById('root')).render(

  <StrictMode>

    <BrowserRouter>

      <Routes>

        <Route path="/" element={<Landing />} />

        <Route path="/auth/callback" element={<AuthCallback />} />

        <Route path="/app" element={

          <ProtectedRoute>

            <App />

          </ProtectedRoute>

        } />

      </Routes>

    </BrowserRouter>

  </StrictMode>

) 

