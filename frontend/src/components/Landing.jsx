import { useNavigate } from 'react-router-dom'
import { supabase } from '../supabaseClient'



export default function Landing() {

  const navigate = useNavigate()
  const handleLogin = async () => {

  await supabase.auth.signInWithOAuth({

    provider: 'google',

    options: {

      redirectTo: `${window.location.origin}/auth/callback`

    }

  })

} 



  return (

    <div className="landing">

      <nav className="landing-nav">

        <div className="landing-logo">

          <div className="landing-logo-mark">🎮</div>

          Game<span className="landing-highlight">Vision</span> IA

        </div>

        <button className="landing-nav-cta" onClick={handleLogin}>

          Ir a la aplicación

        </button>

      </nav>



      <section className="landing-hero">

        <div className="landing-badge">

          <div className="landing-pulse"></div>

          Proyecto de pre-especialización en IA · UGB 2026

        </div>



        <h1 className="landing-h1">

          Predice el potencial<br />

          <span className="landing-grad">comercial</span> de tu idea de videojuego<br />

          antes de empezar a desarrollarla

        </h1>



        <p className="landing-sub">

          GameVision IA utilza un modelo de predicción que se entreno con datos históricos reales de Steam para estimar la probabilidad

          de éxito de tu idea de videojuego, ayudándote a tomar decisiones informadas sobre

          precio, género, si sera gratis o no y fecha de lanzamiento.

        </p>



        <div className="landing-ctas">

          <button className="landing-btn-primary" onClick={handleLogin}>

            Analizar mi juego

          </button>

          <a className="landing-btn-secondary" href="#como-funciona">

            Cómo funciona

          </a>

        </div>



        <div className="landing-preview">

          <div className="landing-preview-bar">

            <div className="landing-preview-dot"></div>

            <div className="landing-preview-dot"></div>

            <div className="landing-preview-dot"></div>

          </div>

          <div className="landing-preview-grid">

            <div className="landing-preview-card">

              <div className="landing-preview-label">Géneros seleccionados</div>

              <div className="landing-chip-row">

                <span className="landing-chip active">Indie</span>

                <span className="landing-chip active">Action</span>

                <span className="landing-chip">RPG</span>

                <span className="landing-chip">Casual</span>

              </div>

              <div className="landing-chip-row">

                <span className="landing-chip active">Single-player</span>

                <span className="landing-chip">Multi-player</span>

                <span className="landing-chip">Co-op</span>

              </div>

            </div>

            <div className="landing-preview-card">

              <div className="landing-preview-label">Resultado del análisis</div>

              <div className="landing-gauge-row">

                <div className="landing-gauge-circle">

                  <div className="landing-gauge-inner">66%</div>

                </div>

                <div className="landing-gauge-text">

                  <div className="landing-gauge-level">Potencial Medio</div>

                  <div className="landing-gauge-sub">prob. de éxito estimada</div>

                </div>

              </div>

            </div>

          </div>

        </div>

      </section>



      <section className="landing-section" id="como-funciona">

        <div className="landing-tag">Proceso</div>

        <h2 className="landing-section-title">Tres pasos hacia una decisión informada</h2>

        <p className="landing-section-sub">Sin necesidad de conocimientos técnicos, obtén un análisis basado en datos reales en segundos.</p>

        <div className="landing-steps">

          <div className="landing-step-card">

            <div className="landing-step-num">01</div>

            <h3>Describe tu juego</h3>

            <p>Selecciona géneros, modos de juego, precio estimado y fecha de lanzamiento mediante un formulario simple e intuitivo.</p>

          </div>

          <div className="landing-step-card">

            <div className="landing-step-num">02</div>

            <h3>Recibe la predicción</h3>

            <p>Un modelo de Machine Learning entrenado con más de 58,000 juegos reales de Steam estima tu probabilidad de éxito comercial.</p>

          </div>

          <div className="landing-step-card">

            <div className="landing-step-num">03</div>

            <h3>Explora con el asistente</h3>

            <p>Conversa con GameVision Assistant para entender el resultado y explorar cómo distintos ajustes podrían mejorarlo.</p>

          </div>

        </div>

      </section>



      {/* --- STACK TECNOLÓGICO --- */}
      <div style={{ paddingTop: '80px' }}>
        <div className="landing-tag" style={{ marginBottom: '10px' }}>Arquitectura</div>
        <h2 className="landing-section-title" style={{ fontSize: '28px', marginBottom: '30px' }}>
          Tecnologías que impulsan el motor
        </h2>
        
        <div className="landing-tech-strip">
          {['Random Forest','Scikit-learn','FastAPI','React + Vite','Gemini 2.5 Flash','LangChain','Supabase'].map(t => (
            <div key={t} className="landing-tech-item">
              <div className="landing-tech-dot"></div>{t}
            </div>
          ))}
        </div>
      </div>


      <section className="landing-section">

        <div className="landing-tag">Capacidades</div>

        <h2 className="landing-section-title">Dos inteligencias trabajando juntas</h2>

        <p className="landing-section-sub">Machine Learning para predecir, lenguaje natural para interpretar.</p>

        <div className="landing-features">

          <div className="landing-feature-card">

            <div className="landing-feature-icon icon-purple">🌲</div>

            <h4>Modelo predictivo</h4>

            <p>Random Forest entrenado con datos históricos reales de Steam, optimizado para manejar el desbalance natural entre juegos exitosos y no exitosos.</p>

          </div>

          <div className="landing-feature-card">

            <div className="landing-feature-icon icon-pink">💬</div>

            <h4>Asistente conversacional</h4>

            <p>Interpreta tu resultado en lenguaje natural y responde preguntas específicas sobre cómo mejorar el potencial comercial de tu juego en Steam.</p>

          </div>

          <div className="landing-feature-card">

            <div className="landing-feature-icon icon-teal">📊</div>

            <h4>Historial de análisis</h4>

            <p>Guarda cada predicción realizada para que puedas comparar distintos escenarios y retomar conversaciones anteriores cuando quieras.</p>

          </div>

        </div>

      </section>



      <section className="landing-section">

        <div className="landing-honesty">

          <div className="landing-honesty-icon">⚖️</div>

          <h3>Una herramienta de apoyo, no un oráculo</h3>

          <p>GameVision IA estima probabilidades basándose en patrones históricos del mercado de Steam. No garantiza resultados ni evalúa la calidad creativa de tu juego. Es un punto de partida para decisiones más informadas, no un sustituto del criterio del desarrollador.</p>

        </div>

      </section>



      <section className="landing-footer-cta">

        <h2>Validá tu idea antes de invertir en ella</h2>

        <p>Decisiones de diseño comercial respaldadas por datos reales, no por intuición.</p>

        

      </section>



      <footer className="landing-footer">

        <div className="landing-logo">🎮 GameVision IA</div>

        <div>Proyecto académico — Pre-especialización en IA · UGB 2026</div>

      </footer>

    </div>

  )

}