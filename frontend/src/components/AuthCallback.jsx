import { useEffect } from 'react'

import { useNavigate } from 'react-router-dom'

import { supabase } from '../supabaseClient'



export default function AuthCallback() {

  const navigate = useNavigate()



  useEffect(() => {

    const { data: { subscription } } = supabase.auth.onAuthStateChange((event, session) => {

      if (event === 'SIGNED_IN' && session) {

        navigate('/app', { replace: true })

      }

    })



    supabase.auth.getSession().then(({ data: { session } }) => {

      if (session) navigate('/app', { replace: true })

    })



    return () => subscription.unsubscribe()

  }, [navigate])



  return (

    <div style={{

      display: 'flex', flexDirection: 'column',

      alignItems: 'center', justifyContent: 'center',

      height: '100vh', gap: '16px',

      background: '#1a1a2e', color: '#D9D9D9'

    }}>

      <div style={{ fontSize: '2rem' }}>🎮</div>

      <p style={{ opacity: 0.7 }}>Iniciando sesión...</p>

    </div>

  )

} 

