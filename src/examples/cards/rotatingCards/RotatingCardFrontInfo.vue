<script setup>
defineProps({
  image: {
    type: String,
    required: true,
  },
  label: {
    type: String,
    default: "",
  },
  title: {
    type: String,
    required: true,
  },
  description: {
    type: String,
    required: true,
  },
  label: {
    type: String,
    required: true,
  },
});
</script>
<template>
  <div
    class="front-info front-background"
    :style="{
      backgroundImage: `url(${image})`,
      backgroundSize: 'cover',
    }"
  >
    <div class="card-body py-5 text-center">
      <a class="d-block blur-shadow-image">
        <img src="../../../assets/img/illustrations/konsultasi.png" width="40%" class="img-fluid border-radius-lg" />
      </a>
      <h3 class="text-white" v-html="title" />
      <p class="text-white opacity-9">
        {{ description }}
      </p>
      <p
        v-if="label"
        class="text-sm text-white font-weight-bold"
      >
        {{ label }}
      </p>
    </div>
  </div>
</template>
