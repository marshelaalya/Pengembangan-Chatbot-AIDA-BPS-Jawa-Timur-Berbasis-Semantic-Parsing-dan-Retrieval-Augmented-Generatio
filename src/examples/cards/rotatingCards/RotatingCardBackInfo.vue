<script setup>
import { RouterLink } from 'vue-router';

const props = defineProps({
  image: {
    type: String,
    required: true,
  },
  title: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    required: true,
  },
  action: {
    type: Array,
    required: true,
  },
});
</script>

<template>
  <div
    class="back-info back-background"
    :style="{
      backgroundImage: `url(${props.image})`,
      backgroundSize: 'cover',
    }"
  >
    <div class="card-body pt-5 text-center">
      <a class="d-block blur-shadow-image">
        <img src="../../../assets/img/illustrations/jadwal.png" width="40%" class="img-fluid mb-2 border-radius-lg" />
      </a>
      <p class="text-white">
        {{ props.description }}
      </p>
      <div class="buttons-group">
        <RouterLink
          v-for="({ route, color, label }, index) in props.action"
          :key="index"
          :to="route"
          class="btn btn-sm mt-3 inline-block ms-1"
          :class="`${color ? `btn-${color}` : 'btn-white'}`"
        >
          {{ label }}
        </RouterLink>
      </div>
    </div>
  </div>
</template>
