<script setup>
defineProps({
  label: {
    type: String,
    default: "",
  },
  active: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  prev: {
    type: Boolean,
    default: false,
  },
  next: {
    type: Boolean,
    default: false,
  },
});
function getClasses(active, disabled) {
  let activeValue, disabledValue;

  activeValue = active && "active";
  disabledValue = disabled && "disabled";

  return `${activeValue} ${disabledValue}`;
}
</script>
<template>
  <li class="page-item" :class="getClasses(active, disabled)">
    <a class="page-link" href="javascript:;">
      <span aria-hidden="true" :class="active ? 'text-white' : ''">
        {{ prev || next ? null : label }}
        <!-- SVG custom untuk prev -->
        <svg
          v-if="prev"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="currentColor"
          class="icon-prev"
          style="width: 1rem; height: 1rem;"
        >
          <path
            d="M15.41 16.59L10.83 12l4.58-4.59L14 6l-6 6 6 6z"
          />
        </svg>

        <!-- SVG custom untuk next -->
        <svg
          v-if="next"
          xmlns="http://www.w3.org/2000/svg"
          viewBox="0 0 24 24"
          fill="currentColor"
          class="icon-next"
          style="width: 1rem; height: 1rem;"
        >
          <path
            d="M8.59 16.59L13.17 12 8.59 7.41 10 6l6 6-6 6z"
          />
        </svg>
      </span>
    </a>
  </li>
</template>
