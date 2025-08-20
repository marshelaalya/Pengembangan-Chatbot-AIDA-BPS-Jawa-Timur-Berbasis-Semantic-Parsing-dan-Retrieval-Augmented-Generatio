<script setup>
defineProps({
  image: {
    type: String,
    required: true,
  },
  title: {
    type: String,
    requierd: true,
  },
  description: {
    type: String,
    required: true,
  },
  url: {
    type: String,
    required: true,
  },
  action: {
    type: Object,
    route: String,
    label: String,
    color: String,
    default: () => ({
      route: "javascript:;",
      label: "Menuju Layanan",
      color: "gray-800",
    }),
  },
});
</script>
<template>
  <div class="info-horizontal border-radius-xl d-block d-md-flex bg-gray-300">
    <div class="card-body justify-content-center text-center">
      <a class="d-block blur-shadow-image">
        <img :src="image" width="40%" class="img-fluid mb-2 border-radius-lg" />
      </a>
      <div class="text-gray-800">
        <h5 class="card-title" style="margin-bottom: 0;">{{ title }}</h5>
        <p class="card-description text-sm text-gray-900 font-weight-normal">
          {{ description }}
        </p>
        <a
          :href="url"
          class="text-sm icon-move-right"
          :class="`text-${action.color}`"
          >{{ action.label }}
          <i class="fas fa-arrow-right text-xs ms-1"></i>
        </a>
      </div>
    </div>
  </div>
</template>
