
<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios' // Importa axios
import Seesaw from './components/Seesaw.vue' // Importa el componente del balancín

// --- Estado Reactivo ---
const lastPayer = ref(null) // Quién pagó último ('YOUR_NAME', 'FRIEND_NAME', null)
const isLoading = ref(true)
const errorMsg = ref('')

// --- Nombres (¡¡IMPORTANTE!! Edita estos valores) ---
// Deben coincidir exactamente con los del backend (app.py)
const friend1 = "CAÑO"  // <-- CAMBIA ESTO
const friend2 = "BARRIO" // <-- CAMBIA ESTO

// --- URL de la API (ajusta si es necesario) ---
const apiUrl = 'http://localhost:5000/api' // O la IP/dominio de tu backend

// --- Lógica ---
// Función para obtener el último pagador al cargar
const fetchLastPayer = async () => {
  isLoading.value = true
  errorMsg.value = ''
  try {
    // Añadimos un timestamp para evitar caché en algunas configuraciones
    const response = await axios.get(`${apiUrl}/last_payer?t=${Date.now()}`)
    lastPayer.value = response.data.last_payer
    console.log("Último pagador recibido:", lastPayer.value)
  } catch (error) {
    console.error("Error al obtener el último pagador:", error.response?.data || error.message)
    errorMsg.value = `Error al conectar con el servidor (${apiUrl}). ¿Está el backend funcionando?`
  } finally {
    isLoading.value = false
  }
}

// Función para registrar un pago
const pay = async (payerName) => {
  isLoading.value = true // Mostrar feedback mientras se procesa
  errorMsg.value = ''
  try {
    const response = await axios.post(`${apiUrl}/pay`, { payer_name: payerName })
    if (response.data.success) {
        lastPayer.value = payerName // Actualiza el estado local inmediatamente
        console.log("Pago registrado por:", payerName)
    } else {
        // Esto no debería ocurrir si el backend devuelve un error HTTP, pero por si acaso
        errorMsg.value = response.data.error || 'Error desconocido al registrar el pago.'
    }
  } catch (error) {
    console.error("Error al registrar el pago:", error.response?.data || error.message)
    errorMsg.value = `Error al registrar el pago: ${error.response?.data?.error || error.message}`
  } finally {
    isLoading.value = false
  }
}

// --- Ciclo de vida ---
onMounted(() => {
  fetchLastPayer() // Llama a la API cuando el componente se monta
})

// --- Propiedades Computadas (para el balancín) ---
const seesawState = computed(() => {
  if (!lastPayer.value) {
    return 'balanced' // Estado inicial o sin pagos
  } else if (lastPayer.value === friend1) {
    return 'left' // Inclinado hacia la izquierda (Amigo 1)
  } else if (lastPayer.value === friend2) {
    return 'right' // Inclinado hacia la derecha (Amigo 2)
  } else {
    return 'balanced'; // Estado por defecto si el nombre no coincide (puede indicar error)
  }
})
</script>

<template>
  <div class="coffee-tracker">
    <h1>¿Quién pagó el último café?</h1>

    <div v-if="isLoading && !lastPayer" class="loading">Consultando el oráculo cafetero...</div>
    <div v-if="errorMsg" class="error">
        <p><strong>¡Ups! Algo fue mal:</strong></p>
        <p>{{ errorMsg }}</p>
    </div>


    <div v-show="!isLoading || lastPayer" class="content"> <!-- Usamos v-show para mantener el layout-->
      <!-- Pasa el estado calculado al componente del balancín -->
      <Seesaw :state="seesawState" :friend1Name="friend1" :friend2Name="friend2" />

      <div class="buttons">
        <button @click="pay(friend1)" :disabled="isLoading">Pagué Yo ({{ friend1 }})</button>
        <button @click="pay(friend2)" :disabled="isLoading">Pagó {{ friend2 }}</button>
      </div>

       <p v-if="lastPayer && !isLoading" class="status-message">
         ¡El último café lo pagó <strong>{{ lastPayer }}</strong>!
       </p>
       <p v-else-if="!lastPayer && !isLoading && !errorMsg" class="status-message">
         ¡Nadie ha pagado todavía! ¿A quién le toca el honor?
       </p>
       <p v-if="isLoading && lastPayer" class="status-message loading">
            Actualizando quién pagó...
       </p>
    </div>
  </div>
</template>

<style scoped>
.coffee-tracker {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: sans-serif;
  padding: 2rem;
  max-width: 600px;
  margin: 2rem auto;
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
}

h1 {
  color: #6F4E37; /* Coffee brown */
  margin-bottom: 2rem;
}

.loading, .error {
   margin: 2rem 0;
   padding: 1rem;
   border-radius: 5px;
}
.loading {
   font-weight: bold;
   color: #495057;
}
.error {
    color: #721c24; /* Dark red */
    background-color: #f8d7da; /* Light red */
    border: 1px solid #f5c6cb; /* Red border */
}
.error p {
    margin-bottom: 0.5rem;
}

.content {
    display: flex;
    flex-direction: column;
    align-items: center;
    width: 100%;
    margin-top: 1rem; /* Add some space if loading indicator was shown */
}

.buttons {
  margin-top: 2.5rem; /* Más espacio después del balancín */
  display: flex;
  gap: 1rem; /* Espacio entre botones */
}

button {
  padding: 0.8rem 1.5rem;
  font-size: 1rem;
  cursor: pointer;
  border: none;
  border-radius: 5px;
  background-color: #A0522D; /* Sienna brown */
  color: white;
  transition: background-color 0.2s ease, opacity 0.2s ease;
}

button:hover {
  background-color: #8B4513; /* Saddle brown */
}
button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
  opacity: 0.7;
}


.status-message {
  margin-top: 1.5rem;
  font-size: 1.1rem;
  color: #495057;
  min-height: 1.5em; /* Reserve space to avoid layout jump */
}
.status-message strong {
  color: #28a745; /* Un color destacado para el pagador */
  font-weight: bold;
}
.status-message.loading {
    font-style: italic;
}
</style>
