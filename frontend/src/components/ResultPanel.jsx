import { useEffect, useState } from 'react'


const getLevelColor = (level) => {

  if (level === 'Alto') return '#4ecdc4'

  if (level === 'Medio') return '#f7b731'

  return '#fc5c65'

}



const getLevelEmoji = (level) => {

  if (level === 'Alto') return '🚀'

  if (level === 'Medio') return '►'

  return '⚠️'

}



export default function ResultPanel({ prediction }) {

  const [animatedValue, setAnimatedValue] = useState(0)

  const percentage = Math.round(prediction.probability * 100)

  const color = getLevelColor(prediction.potential_level)



  useEffect(() => {

    setAnimatedValue(0)

    const timer = setTimeout(() => setAnimatedValue(percentage), 100)

    return () => clearTimeout(timer)

  }, [prediction])



  const radius = 80

  const circumference = 2 * Math.PI * radius

  const offset = circumference - (animatedValue / 100) * circumference



  return (

    <div className="result-card">

      <h2 className="result-title">Resultado del análisis</h2>



      <div className="gauge-container">

        <svg width="200" height="200" viewBox="0 0 200 200">

          <circle

            cx="100" cy="100" r={radius}

            fill="none"

            stroke="#2a2a4a"

            strokeWidth="16"

          />

          <circle

            cx="100" cy="100" r={radius}

            fill="none"

            stroke={color}

            strokeWidth="16"

            strokeDasharray={circumference}

            strokeDashoffset={offset}

            strokeLinecap="round"

            transform="rotate(-90 100 100)"

            style={{ transition: 'stroke-dashoffset 1s ease' }}

          />

          <text x="100" y="95" textAnchor="middle" fill={color} fontSize="28" fontWeight="bold">

            {animatedValue}%

          </text>

          <text x="100" y="118" textAnchor="middle" fill="#888" fontSize="12">

            probabilidad

          </text>

        </svg>

      </div>



      <div className="level-badge" style={{ borderColor: color, color }}>

        {getLevelEmoji(prediction.potential_level)} Potencial {prediction.potential_level}

      </div>



      <div className="result-details">

        <div className="detail-item">

          <span className="detail-label">Clasificación</span>

          <span className="detail-value" style={{ color }}>

            {prediction.predicted_class === 1 ? 'Exitoso' : 'No exitoso'}

          </span>

        </div>

        <div className="detail-item">

          <span className="detail-label">Probabilidad exacta</span>

          <span className="detail-value">{(prediction.probability * 100).toFixed(2)}%</span>

        </div>

      </div>

    </div>

  )

} 

