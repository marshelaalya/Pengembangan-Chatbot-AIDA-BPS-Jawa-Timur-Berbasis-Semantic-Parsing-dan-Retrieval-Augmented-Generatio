<template>
  <div class="container-fluid py-3" style="background-color: #407bff">
    <div class="row height d-flex justify-content-center align-items-center">
      <div class="col-md-8">
        <div class="search">
          <input
            type="text"
            class="form-control rounded-3"
            placeholder="Mau cari data apa?"
            v-model="searchQuery"
            @keyup.enter="performSearch"
            style="background-color: #eee"
          />
          <button class="btn rounded-3" id="btnSearch" @click="performSearch">Cari</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "SearchComponent",
  props: {
    initialSearchQuery: {
      type: String,
      default: ''
    }
  },
  data() {
    return {
      searchQuery: this.initialSearchQuery
    };
  },
  watch: {
    initialSearchQuery(newQuery) {
      // When initialSearchQuery changes, update searchQuery
      this.searchQuery = newQuery;
      // Automatically perform search
      this.performSearch();
    }
  },
  methods: {
    performSearch() {
      const trimmedQuery = this.searchQuery.trim();
      // Emit the trimmed search query to the parent
      this.$emit('search-updated', trimmedQuery);
      // Update the router with the search query
      if (trimmedQuery) {
        this.$router.push({ name: 'search', query: { searchQuery: trimmedQuery } });
      }
    }
  }
};
</script>

<style>
body {
  background-color: #eee;
  font-family: "Poppins", sans-serif;
  font-weight: 300;
}

.height {
  height: fit-content;
}

.search {
  position: relative;
  box-shadow: 0 0 40px rgba(51, 51, 51, 0.1);
}

.search input {
  height: 50px;
  text-indent: 15px;
  border: 2px solid #d6d4d4;
}

.search input:focus {
  box-shadow: none;
  border: 2px solid rgb(60, 59, 59);
}

#btnSearch {
  position: absolute;
  top: 5px;
  right: 5px;
  height: 40px;
  width: 100px;
  background-color: #e4561d;
  color: #eee;
  border: none;
  cursor: pointer;
}

#btnSearch:hover {
  background-color: #d2451a;
}
</style>
