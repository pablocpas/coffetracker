
<script setup>
import { computed } from 'vue'

// Propiedades que recibe este componente desde App.vue
const props = defineProps({
  state: { // 'balanced', 'left', 'right'
    type: String,
    required: true,
    default: 'balanced',
    validator: (value) => ['balanced', 'left', 'right'].includes(value)
  },
  friend1Name: {
    type: String,
    required: true
  },
  friend2Name: {
    type: String,
    required: true
  }
})

// Clase CSS dinámica basada en el estado
const seesawClass = computed(() => {
  return {
    'seesaw-plank': true,
    'state-balanced': props.state === 'balanced',
    'state-left': props.state === 'left',
    'state-right': props.state === 'right'
  }
})

// Ajuste de rotación inversa para mantener los monigotes verticales
const personLeftStyle = computed(() => ({
  transform: props.state === 'right' ? 'rotate(-10deg)' : (props.state === 'left' ? 'rotate(10deg)' : 'rotate(0deg)')
}));

const personRightStyle = computed(() => ({
  transform: props.state === 'right' ? 'rotate(-10deg)' : (props.state === 'left' ? 'rotate(10deg)' : 'rotate(0deg)')
}));

</script>

<template>
  <div class="seesaw-container">
    <div :class="seesawClass">
      <!-- Monigote Izquierda (Amigo 1) -->
      <div class="person person-left" :style="personLeftStyle">
        <div class="head"></div>
        <div class="body"></div>
        <span class="name">{{ friend1Name }}</span>
      </div>

      <!-- Monigote Derecha (Amigo 2) -->
      <div class="person person-right" :style="personRightStyle">
         <div class="head"></div>
         <div class="body friend2-body"></div> <!-- Clase específica para el color del amigo 2 -->
         <span class="name">{{ friend2Name }}</span>
      </div>
    </div>
    <div class="seesaw-base"></div>
  </div>
</template>

<style scoped>
.seesaw-container {
  width: 90%; /* Usar porcentaje para mejor responsividad */
  max-width: 400px; /* Limitar ancho máximo */
  min-width: 280px; /* Ancho mínimo */
  height: 150px; /* Altura suficiente para el movimiento */
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 2rem 0; /* Espacio arriba y abajo */
  position: relative; /* Para posicionar la base */
}

.seesaw-plank {
  width: 100%;
  height: 20px;
  background: linear-gradient(to bottom, #A0522D, #8B4513); /* Gradiente madera */
  border-radius: 10px; /* Más redondeado */
  position: relative; /* Para posicionar los monigotes */
  transition: transform 0.5s cubic-bezier(0.68, -0.55, 0.27, 1.55); /* Animación con rebote */
  transform-origin: center bottom; /* Pivote en el centro inferior */
  z-index: 1; /* Por encima de la base */
  margin-bottom: -10px; /* Solapar un poco con la base */
  box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

/* Estados de inclinación */
.state-balanced {
  transform: rotate(0deg);
}
.state-left {
  transform: rotate(-10deg); /* Inclinación izquierda */
}
.state-right {
  transform: rotate(10deg); /* Inclinación derecha */
}

.seesaw-base {
  width: 0;
  height: 0;
  border-left: 35px solid transparent; /* Base un poco más ancha */
  border-right: 35px solid transparent;
  border-bottom: 55px solid #888; /* Base gris más oscura */
  position: relative;
  z-index: 0; /* Detrás de la tabla */
  align-self: center; /* Asegura que esté centrado */
  filter: drop-shadow(0 3px 3px rgba(0,0,0,0.3)); /* Sombra para la base */
}

/* Estilos para los monigotes (simples) */
.person {
  position: absolute;
  bottom: 18px; /* Ligeramente más arriba de la tabla */
  display: flex;
  flex-direction: column;
  align-items: center;
  /* La transición de rotación inversa se aplica directamente con :style */
  transition: transform 0.5s cubic-bezier(0.68, -0.55, 0.27, 1.55); /* Misma animación */
  transform-origin: bottom center; /* Rotar sobre los pies */
}

.person-left {
  left: 10%; /* Posición relativa */
}
.person-right {
  right: 10%; /* Posición relativa */
}

.head {
  width: 30px;
  height: 30px;
  background: #FFE0BD; /* Color piel más cálido */
  border-radius: 50%;
  border: 1px solid #aaa;
  box-shadow: inset 0 -2px 3px rgba(0,0,0,0.1); /* Sombra interior ligera */
}

.body {
  width: 25px;
  height: 40px;
  background-color: #3498db; /* Azul */
  border-radius: 15px 15px 0 0; /* Más redondeado arriba */
  margin-top: -5px;
  border: 1px solid #2980b9;
  border-bottom: none;
}

.friend2-body {
    background-color: #e74c3c; /* Rojo */
    border-color: #c0392b;
}

.name {
  margin-top: 5px;
  font-size: 0.8rem;
  font-weight: bold;
  color: #333;
  background-color: rgba(255, 255, 255, 0.8); /* Fondo semitransparente */
  padding: 2px 5px;
  border-radius: 3px;
  box-shadow: 0 1px 1px rgba(0,0,0,0.1);
  white-space: nowrap; /* Evitar que el nombre se parta */
}
</style>
