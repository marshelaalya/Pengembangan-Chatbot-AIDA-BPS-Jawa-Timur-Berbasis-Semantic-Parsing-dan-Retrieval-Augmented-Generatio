import '@fontsource/fira-code';
import { createApp } from "vue";
import { createPinia } from "pinia";
import App from "./App.vue";
import router from "./router";
import store from './store'
import gAuthPlugin from "vue3-google-login";
import VueSweetalert2 from 'vue-sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';
import "@/assets/styles/code.css";
let CLIENT_ID =
  "320659382153-hsbpa3c5oop22n0c9jsqjau4enj80svp.apps.googleusercontent.com";

// Nucleo Icons
import "./assets/css/nucleo-icons.css";
import "./assets/css/nucleo-svg.css";
import 'bootstrap-icons/font/bootstrap-icons.css';

import materialKit from "./material-kit";

const app = createApp(App);

app.use(gAuthPlugin, {
  clientId: CLIENT_ID,
});

app.use(createPinia());
app.use(router);
app.use(store)
app.use(materialKit);
app.use(VueSweetalert2);

app.mount("#app");
