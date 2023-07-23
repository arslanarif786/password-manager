<template>
  <v-layout style="min-height: 100vh; max-height: 500vh">
    <Sidebar />
    <v-main class="bg-white">
      <div class="text-right mt-5 mr-4">
        <v-avatar color="text-white secondary-color">
          <v-icon icon="mdi-account-circle" color="white"></v-icon>
        </v-avatar>
      </div>
      <MainTable />
    </v-main>
  </v-layout>
</template>

<script setup>
import Sidebar from "@/layouts/Sidebar.vue";
import MainTable from "@/components/MainTable.vue";
</script>
