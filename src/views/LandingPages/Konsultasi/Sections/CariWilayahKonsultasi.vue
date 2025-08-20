<template>
  <div class="select-container">
    <div class="input-container">
      <input
        type="text"
        class="select-input"
        v-model="searchQuery"
        @click="toggleOptions"
        @input="filterOptions"
        placeholder="Cari wilayah..."
      />
      <i class="fa fa-search search-icon" aria-hidden="true"></i>
    </div>
    <ul v-if="showOptions" class="options-list">
      <li
        v-for="(option, index) in visibleOptions"
        :key="index"
        class="option-item"
        @click="selectOption(option)"
      >
        {{ option.label }}
      </li>
      <li v-if="filteredOptions.length > maxOptionsToShow" class="option-item show-more" @click="showAllOptions">
        Show more...
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: '',
      options: [
        { label: "Jawa Timur", value: "3500" },
        { label: "Kab. Bangkalan", value: "3526" },
        { label: "Kab. Banyuwangi", value: "3510" },
        { label: "Kab. Blitar", value: "3505" },
        { label: "Kab. Bojonegoro", value: "3522" },
        { label: "Kab. Bondowoso", value: "3511" },
        { label: "Kab. Gresik", value: "3525" },
        { label: "Kab. Jember", value: "3509" },
        { label: "Kab. Jombang", value: "3517" },
        { label: "Kab. Kediri", value: "3506" },
        { label: "Kab. Lamongan", value: "3524" },
        { label: "Kab. Lumajang", value: "3508" },
        { label: "Kab. Madiun", value: "3519" },
        { label: "Kab. Magetan", value: "3520" },
        { label: "Kab. Malang", value: "3507" },
        { label: "Kab. Mojokerto", value: "3516" },
        { label: "Kab. Nganjuk", value: "3518" },
        { label: "Kab. Ngawi", value: "3521" },
        { label: "Kab. Pacitan", value: "3501" },
        { label: "Kab. Pamekasan", value: "3528" },
        { label: "Kab. Pasuruan", value: "3514" },
        { label: "Kab. Ponorogo", value: "3502" },
        { label: "Kab. Probolinggo", value: "3513" },
        { label: "Kab. Sampang", value: "3527" },
        { label: "Kab. Sidoarjo", value: "3515" },
        { label: "Kab. Situbondo", value: "3512" },
        { label: "Kab. Sumenep", value: "3529" },
        { label: "Kab. Trenggalek", value: "3503" },
        { label: "Kab. Tuban", value: "3523" },
        { label: "Kab. Tulungagung", value: "3504" },
        { label: "Kota Batu", value: "3579" },
        { label: "Kota Blitar", value: "3572" },
        { label: "Kota Kediri", value: "3571" },
        { label: "Kota Madiun", value: "3577" },
        { label: "Kota Malang", value: "3573" },
        { label: "Kota Mojokerto", value: "3576" },
        { label: "Kota Pasuruan", value: "3575" },
        { label: "Kota Probolinggo", value: "3574" },
        { label: "Kota Surabaya", value: "3578" },
      ],
      showOptions: false,
      maxOptionsToShow: 5,
      showAll: false
    };
  },
  computed: {
    filteredOptions() {
      return this.options.filter(option =>
        option.label.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
    visibleOptions() {
      return this.showAll ? this.filteredOptions : this.filteredOptions.slice(0, this.maxOptionsToShow);
    }
  },
  methods: {
    toggleOptions() {
      if (this.showOptions) {
        this.showAll = false;
      }
      this.showOptions = !this.showOptions;
    },
    filterOptions() {
      this.showOptions = true;
      this.showAll = false;
    },
    selectOption(option) {
      this.searchQuery = option.label;
      this.showOptions = false;
      this.showAll = false;
      this.$emit('data', option.value); // Emit the selected option's value
    },
    showAllOptions() {
      this.showAll = true;
    }
  }
};
</script>

<style scoped>
.select-container {
  position: relative;
  width: 250px;
}

.input-container {
  position: relative;
}

.select-input {
  width: 100%;
  padding: 8px 30px 8px 8px;
}

.search-icon {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
}

.options-list {
  list-style-type: none;
  padding: 0;
  margin: 0;
  position: absolute;
  top: calc(100% + 5px);
  left: 0;
  width: 100%;
  border: 1px solid #ccc;
  border-top: none;
  border-radius: 0 0 5px 5px;
  background-color: #fff;
  z-index: 1;
}

.option-item {
  padding: 8px;
  cursor: pointer;
}

.option-item:hover {
  background-color: #f0f0f0;
}

.show-more {
  text-align: center;
  font-weight: bold;
}
</style>
