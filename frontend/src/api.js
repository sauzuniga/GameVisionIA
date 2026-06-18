 import axios from 'axios'



const API = axios.create({

  baseURL: 'http://localhost:8000/api'

})



export const predictGame = async (gameData) => {

  const response = await API.post('/predict', gameData)

  return response.data

}



export const sendChatMessage = async (sessionId, message, predictionContext) => {

  const response = await API.post('/chat', {

    session_id: sessionId,

    message,

    prediction_context: predictionContext

  })

  return response.data

}



export const getChatMessages = async (sessionId) => {

  const response = await API.get(`/chat/${sessionId}/messages`)

  return response.data

}



export const getHistory = async () => {

  const response = await API.get('/history')

  return response.data

}



export const getPrediction = async (predictionId) => {

  const response = await API.get(`/history/${predictionId}`)

  return response.data

} 

