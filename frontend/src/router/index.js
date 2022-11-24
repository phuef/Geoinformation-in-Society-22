import Vue from "vue";
import VueRouter from "vue-router";
import ImpressumView from "../components/ImpressumView.vue";
import MainPage from "../components/MainPage.vue";
//import MapView from "../components/MapView.vue";
//import MapTmp from "../components/MapTmp.vue";
Vue.use(VueRouter);
const routes = [
  {
    path: "/impressum",
    name: "ImpressumView",
    component: ImpressumView,
  },
  {
    path: "/main",
    name: "Main",
    component: MainPage,
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
