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

      <img :src="image" width="35%" class="img-fluid border-radius-lg mb-2" />
      <p class="text-dark" :class="typeof description == 'string' ? 'pe-0' : description.class">
        {{ typeof description == "string" ? description : description.text }}
      </p>
    </div>
  </div>
</template>
