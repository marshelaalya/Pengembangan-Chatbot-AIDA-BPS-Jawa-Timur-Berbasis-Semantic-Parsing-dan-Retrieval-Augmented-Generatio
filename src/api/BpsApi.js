import axios from 'axios';

const BPS_API_KEY = '2ad01e6a21b015ea1ff8805ced02600c';
const BASE_URL = 'https://webapi.bps.go.id/v1/api/';

// Membuat instance axios untuk BPS WebAPI
const bpsApiClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Fungsi helper untuk encode parameter URL
const encodeQueryParam = (param) => encodeURIComponent(param);

/**
 * Service untuk mengakses BPS Web API
 * Dokumentasi lengkap dapat dilihat di https://webapi.bps.go.id/documentation
 */
export const bpsApiService = {
  /**
   * Mendapatkan data tabel statistik
   * @param {string} domain - Kode domain wilayah (contoh: 3500 untuk Jawa Timur)
   * @param {string} keyword - Kata kunci pencarian
   * @param {number} page - Nomor halaman (opsional)
   * @returns {Promise} Response dari API berisi data tabel statistik
   */
  getStatisticTable(domain, keyword = '', page = 1) {
    return bpsApiClient.get(
      `list/model/statictable/lang/ind/domain/${domain}/keyword/${encodeQueryParam(keyword)}/key/${BPS_API_KEY}?page=${page}`
    );
  },

  /**
   * Mendapatkan data publikasi
   * @param {string} domain - Kode domain wilayah
   * @param {string} keyword - Kata kunci pencarian
   * @param {number} page - Nomor halaman (opsional)
   * @returns {Promise} Response dari API berisi data publikasi
   */
  getPublications(domain, keyword = '', page = 1) {
    return bpsApiClient.get(
      `list/model/publication/lang/ind/domain/${domain}/keyword/${encodeQueryParam(keyword)}/key/${BPS_API_KEY}?page=${page}`
    );
  },

  /**
   * Mendapatkan berita resmi statistik
   * @param {string} domain - Kode domain wilayah
   * @param {string} keyword - Kata kunci pencarian
   * @param {number} page - Nomor halaman (opsional)
   * @returns {Promise} Response dari API berisi data berita resmi statistik
   */
  getPressReleases(domain, keyword = '', page = 1) {
    return bpsApiClient.get(
      `list/model/pressrelease/lang/ind/domain/${domain}/keyword/${encodeQueryParam(keyword)}/key/${BPS_API_KEY}?page=${page}`
    );
  },

  /**
   * Mendapatkan data berdasarkan model dan domain
   * @param {string} model - Jenis model data (statictable/publication/pressrelease)
   * @param {string} domain - Kode domain wilayah
   * @param {string} keyword - Kata kunci pencarian
   * @param {number} page - Nomor halaman (opsional)
   * @returns {Promise} Response dari API berisi data sesuai model yang dipilih
   */
  getDataByModel(model, domain, keyword = '', page = 1) {
    return bpsApiClient.get(
      `list/model/${model}/lang/ind/domain/${domain}/keyword/${encodeQueryParam(keyword)}/key/${BPS_API_KEY}?page=${page}`
    );
  },

  /**
   * Mendapatkan detail data
   * @param {string} model - Jenis model data
   * @param {string} id - ID data yang ingin diambil
   * @param {string} domain - Kode domain wilayah
   * @returns {Promise} Response dari API berisi detail data
   */
  getDataDetail(model, id, domain) {
    return bpsApiClient.get(
      `view/model/${model}/lang/ind/id/${id}/domain/${domain}/key/${BPS_API_KEY}`
    );
  }
};