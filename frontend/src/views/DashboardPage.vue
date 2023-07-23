<template>
  <v-layout style="min-height: 100vh; max-height: 500vh">
    <Sidebar />
    <v-main class="bg-white">
      <!-- Desktop Screen View -->
      <div v-if="$vuetify.display.lg" class="text-right mt-5 mr-4">
        <v-avatar color="text-white secondary-color">
          <v-icon icon="mdi-account-circle" color="white"></v-icon>
        </v-avatar>
      </div>

      <!-- Tablet and mobile screen view -->
      <v-menu
        v-else
        :location="$vuetify.display.smAndDown ? 'start' : 'bottom'"
      >
        <template v-slot:activator="{ props }">
          <div class="text-right mt-5 mr-4">
            <v-btn
              icon="mdi-account-circle"
              class="text-white secondary-color"
              v-bind="props"
            ></v-btn>
          </div>
        </template>
        <v-list class="py-0">
          <v-list-item v-for="(item, index) in items" :key="index">
            <v-list-item-title class="item-title" @click="logout(item.key)">{{
              item.title
            }}</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>

      <MainTable />
    </v-main>
  </v-layout>
</template>

<script setup>
import { ref } from "vue";
import Sidebar from "@/layouts/Sidebar.vue";
import MainTable from "@/components/MainTable.vue";
import router from "@/router";
const items = ref([
  { title: "Home", key: "home", path: "/" },
  { title: "Logout", key: "logout", path: "/" },
]);
function logout(key) {
  if (key == "logout") {
    localStorage.clear();
  }
  router.push({ path: "/" });
}
</script>

<style scoped>
:deep .v-list-item--density-default {
  min-height: 30px;
}
.item-title:hover {
  color: orangered;
}
</style>
