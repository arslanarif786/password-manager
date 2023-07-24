<template>
  <v-card>
    <v-layout style="min-height: 100vh">
      <v-navigation-drawer style="position: fixed;" class="secondary-color">
        <h1 class="text-white text-center mt-4 txt24 font-avenir">
            Password <span class="text-deep-orange font-avenir"> Manager </span>
        </h1>
        <v-list>
          <v-list-item
            prepend-icon="mdi-home"
            title="Home"
            class="cursor-pointer text-white"
            @click="$router.push({path: '/'})"
          ></v-list-item>
          <!-- <v-list-item
            prepend-icon="mdi-view-dashboard"
            title="Dashboard"
            class="cursor-pointer text-white"
          ></v-list-item> -->
        </v-list>

        <template v-slot:append>
          <div class="pa-2">
            <v-btn
              @click="logout"
              block
              variant="outlined"
              color="white"
              class="text-capitalize"
            >
              Logout
            </v-btn>
          </div>
        </template>
      </v-navigation-drawer>
      <v-main></v-main>
    </v-layout>
  </v-card>
</template>

<script setup>
import { useRouter } from "vue-router";
import useToast from '@/plugins/useToast.js'
const router = useRouter();

const logout = () => {
  localStorage.clear();
  useToast("Logout successfully", "success");
  router.push({ path: "/" });
  useT
};
</script>

<style scoped>
:deep .v-list-item__content:hover {
    color: #ff5722 !important;
}
</style>
