<template>
  <a
    href="#"
    class="list-group-item list-group-item-action d-flex gap-3 py-3"
    aria-current="true"
    @click.prevent="$emit('click')"
  >
    <img
      src="@\assets\img\bell.png"
      alt="twbs"
      width="32"
      height="32"
      v-if="notif.read_at!=null"
      class="rounded-circle flex-shrink-0"
    />
    <img
      src="@\assets\img\bell_notif.png"
      alt="twbs"
      width="32"
      height="32"
      v-else
      class="rounded-circle flex-shrink-0"
    />
    <div class="d-flex gap-2 w-100 justify-content-between">
      <div>
        <h6 class="mb-0">Notifikasi Baru</h6>
        <p class="mb-0 opacity-75">{{ truncate(notif.data.message, 50) }}</p>
      </div>
      <small class="opacity-50 text-nowrap">{{ new Date(notif.created_at).toLocaleString() }}</small>
    </div>
  </a>
</template>

<script>
export default {
  props: {
    notif: {
      type: Object,
      required: true,
    },
  },
  methods: {
    truncate(text, length) {
      if (text.length <= length) {
        return text;
      }
      return text.substring(0, length) + '...';
    },
  },
};
</script>
