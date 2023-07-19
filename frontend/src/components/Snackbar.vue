<template>
  <v-sheet class="d-flex flex-column">
    <v-snackbar :timeout="3000" color="deep-purple-accent-4" elevation="24">
      <template v-slot:activator="{ props }">
        <v-btn color="deep-purple-accent-4" class="ma-2" v-bind="props"
          >open</v-btn
        >
      </template>

      Snackbar with <strong>elevation="24"</strong>.
    </v-snackbar>
  </v-sheet>
</template>
