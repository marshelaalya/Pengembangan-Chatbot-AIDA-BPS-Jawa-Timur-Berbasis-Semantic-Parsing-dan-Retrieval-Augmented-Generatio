<script setup>
import { ref, onMounted, defineEmits } from "vue";
import axios from "axios";
import InfoCard from "../../../../examples/cards/infoCards/InfoCard.vue";
import { apiService } from "@/api/ApiService";

const keahlianData = ref([]);

// Emit function to send events to parent component
const emit = defineEmits(['item']);

// Function to handle click event and emit itemId
const clickKeahlian = (itemId) => {
  emit('item', itemId);
  console.log("Keahlian clicked:", itemId);
};

// Fetch data from the API when the component is mounted
onMounted(async () => {
  try {
    const response = await apiService.getKeahlian();
    keahlianData.value = response.data.data;
  } catch (error) {
    console.error("Error fetching keahlian data:", error);
  }
});
</script>

<template>
  <section class="py-0">
    <div class="container">
      <div class="row justify-content-center align-items-top">
        <div
          v-for="item in keahlianData"
          :key="item.id"
          class="col-lg-2 col-6 d-flex justify-content-center"
        >
          <div class="row justify-content-center text-center">
            <InfoCard
              :image="item.icon"
              :description="item.nama_keahlian"
              class=" cursor-pointer"
              @click="clickKeahlian(item.id)"
            />
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
