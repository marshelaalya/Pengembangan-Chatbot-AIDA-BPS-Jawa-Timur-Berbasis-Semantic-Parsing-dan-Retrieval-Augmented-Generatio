<script setup>
defineProps({
  image: {
    type: String,
    required: true,
  },
  description: {
    type: [String, Object],
    required: true,
    text: String,
    class: String,
  },
  col: {
    type: String,
    default: "",
  },
  url: {
    type: String,
    required: true,
  },
});
</script>
<script>
export default {
  inheritAttrs: false,
};
</script>
<template>
  <div :class="`${col ? col : 'col-md-12'}`">
    <div v-bind="$attrs" class="info">
      <a :href="url">
        <img :src="image" width="35%" class="img-fluid border-radius-lg mb-2" />
        <p class="text-white" :class="typeof description == 'string' ? 'pe-0' : description.class">
          {{ typeof description == "string" ? description : description.text }}
        </p>
      </a>
    </div>
  </div>
</template>
