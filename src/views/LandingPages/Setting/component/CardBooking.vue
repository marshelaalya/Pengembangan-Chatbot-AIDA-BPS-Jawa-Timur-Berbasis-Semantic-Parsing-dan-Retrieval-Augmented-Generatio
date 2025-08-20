<template>
  <div>
    <!-- Card booking -->
    <div v-if="!selectedBooking">
      <div class="card border-0 shadow-sm">
        <!-- Konten card booking -->
        <div class="card-header px-4 pt-4 pb-2">
          <h4 class="card-title">Daftar Reservasi</h4>
          <p class="card-text">
            <small class="text-muted mb-4">
              Anda dapat melihat list daftar reservasi yang telah anda buat di
              sini!
            </small>
          </p>
        </div>
        <hr class="hairline mb-0" />
        <div class="card-body m-3">
          <table
            class="table table-bordered"
            v-if="!loading && bookings.length"
          >
            <thead>
              <tr>
                <th scope="col">Tanggal</th>
                <th scope="col">Jam</th>
                <th scope="col">Nama Petugas</th>
                <th scope="col">Status</th>
                <th scope="col">Aksi</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(booking, index) in bookings" :key="index">
                <td>{{ booking.tanggal_konsultasi }}</td>
                <td>{{ booking.waktu_konsultasi }}</td>
                <td>{{ booking.petugas.nama_petugas}}</td>
                <td>
                  <span
                    class="badge bg-warning"
                    v-if="booking.status == 'Diajukan'"
                  >
                    Diajukan
                  </span>
                  <span
                    class="badge bg-info"
                    v-else-if="booking.status == 'Disetujui'"
                  >
                    Disetujui
                  </span>
                </td>
                <td class="d-flex justify-content-center align-items-center">
                  <button
                    class="btn btn-danger btn-sm"
                    @click="showDetail(booking.uuid)"
                  >
                    Detail >>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
          <div class="text-center" v-else-if="loading">
            <img src="/assets/loading_2.svg" alt="Loading..." />
            <p>Loading...</p>
          </div>
          <div class="text-center" v-else>
            <p>Tidak ada reservasi ditemukan.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { apiService } from "@/api/ApiService";

export default {
  name: "CardBooking",
  setup() {
    const bookings = ref([]);
    const loading = ref(true);
    const selectedBooking = ref(null);
    const router = useRouter();

    const fetchBookings = async () => {
      loading.value = true;
      try {
        const storedUser = localStorage.getItem("user");
        const parsedUser = JSON.parse(storedUser);
        if (parsedUser) {
          const response = await apiService.getReservationsByUser(
            parsedUser.id
          );
          const sortedBookings = response.data.data.sort((a, b) => {
            // Sorting descending berdasarkan tanggal_konsultasi
            return (
              new Date(b.tanggal_konsultasi) - new Date(a.tanggal_konsultasi)
            );
          });
          bookings.value = sortedBookings;
        } else {
          throw new Error("User tidak ditemukan di localStorage");
        }
      } catch (error) {
        console.error("Error fetching bookings:", error);
      } finally {
        loading.value = false;
      }
    };

    const showDetail = (bookingUuid) => {
      console.log("booking id" + bookingUuid);
      router.push({
        name: "CardDetailBooking",
        params: { uuid: bookingUuid },
      });
    };

    onMounted(fetchBookings);

    return {
      bookings,
      loading,
      selectedBooking,
      showDetail,
    };
  },
};
</script>

<style scoped>
.hairline {
  width: 100%;
  border: 0;
  border-top: 1px solid #141e2a;
  margin-bottom: 20px;
}
</style>
