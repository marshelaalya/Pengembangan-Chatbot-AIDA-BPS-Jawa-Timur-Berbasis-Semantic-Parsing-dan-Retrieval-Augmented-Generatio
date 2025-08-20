<template>
  <div class="card mb-3 border-0 shadow-sm rounded-4">
    <div class="row g-0 d-flex align-items-center justify-content-center">
      <div class="col-md-4 round mt-2">
        <img :src="user.foto" class="img-fluid rounded-start" height="100px" width="auto" />
      </div>
      <div class="col-md-8">
        <div class="card-body p-3">
          <h5 class="card-title">{{ user.nama_pengguna }}</h5>
          <p class="card-text"><small>{{ user.email_google }}</small></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    user: {
      type: Object,
      
    },
  },
  created(){  
  
    const storedUser = localStorage.getItem("user");
    const storedLoggedIn = localStorage.getItem("loggedIn");

    if (storedUser && storedLoggedIn) {
      const parsedUser = JSON.parse(storedUser);
      console.log(parsedUser)
      // Set user fields with defaults if null or undefined
      this.user.nama_pengguna = parsedUser.nama_pengguna ?? '-';
      this.user.email_google = parsedUser.email_google ?? '-';
      this.user.foto = parsedUser.foto ?? '';
    }
  },
};
</script>

<style scoped>
.round {
  border-radius: 50%;
  overflow: hidden;
  width: 75px;
  height: 75px;
  border: 2px solid white;
}
.round img {
  display: block;
  min-width: 100%;
  min-height: 100%;
}

.table-bordered th,
.table-bordered td {
  border: 1px solid #dee2e6;
}

.table-bordered th {
  vertical-align: middle;
  text-align: left;
}

.table-bordered td {
  padding: 0.5rem;
}
</style>
