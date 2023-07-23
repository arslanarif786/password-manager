<template>
  <v-row justify="center">
    <v-dialog v-model="handleDialog" persistent width="auto">
      <v-card>
        <v-card-text>
          Are you sure you want to delete this account?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="deep-orange" variant="text" @click="closeDialog()">
            No
          </v-btn>
          <v-btn
            color="red"
            variant="flat"
            :loading="loader"
            @click="handleAccount(card.password_id)"
          >
            Yes
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script setup>
import { watch } from "vue";
import { ref } from "vue";
const props = defineProps(["dialog", "card", "buttonLoader"]);
const emit = defineEmits(["handle-delete"]);
const handleDialog = ref(false);
const loader = ref(false)
watch(
  props,
  (newValue) => {
    handleDialog.value = newValue.dialog;
    loader.value = newValue.buttonLoader;
  },
  { immediate: true }
);
function closeDialog() {
  emit("close-delete-popup", false);
}
// attach handle account API here
function handleAccount(id) {
  loader.value = true;
  emit("handle-delete", { cardId: id, key: false, loader: loader.value });
}
</script>
