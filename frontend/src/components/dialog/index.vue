<template>
  <v-row justify="center">
    <v-dialog v-model="handleDialog" persistent width="500">
      <v-card>
        <v-card-title class="mt-3">
          <span v-if="dialogKey == 'add'" class="txt20 ml-6">Add Account</span>
          <span v-else-if="dialogKey == 'edit'" class="txt20 ml-6"
            >Update Account</span
          >
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="cardObject.platform"
                  label="Platform Name*"
                  variant="solo"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="cardObject.username"
                  label="Username*"
                  variant="solo"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="cardObject.password"
                  label="Password*"
                  variant="solo"
                  :type="visible ? 'text' : 'password'"
                  :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
                  @click:append-inner="visible = !visible"
                  required
                ></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="deep-orange"
            variant="text"
            @click="closeDialog"
            class="text-capitalize mb-2"
          >
            Close
          </v-btn>
          <v-btn
            v-if="dialogKey == 'add'"
            color="deep-orange"
            variant="tonal"
            :loading="loader"
            @click="AddNewAccount"
            class="text-capitalize mr-8 mb-2"
          >
            Add
          </v-btn>
          <v-btn
            v-else-if="dialogKey == 'edit'"
            color="deep-orange"
            variant="tonal"
            :loading="loader"
            @click="updateAccount(card.password_id)"
            class="text-capitalize mr-8 mb-2"
          >
            Update
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-row>
</template>

<script setup>
import { watch } from "vue";
import { ref } from "vue";
import { useRouter } from "vue-router";

const props = defineProps(["dialog", "dialogKey", "card", "buttonLoader"]);
const emit = defineEmits(["close-dialog", "add-new-account", "update-account"]);
const handleDialog = ref(false);
const router = useRouter();
const visible = ref(false)
const loader = ref(false)
const cardObject = ref({
  platform: "",
  username: "",
  password: "",
});

watch(
  props,
  (newValue) => {
    handleDialog.value = newValue.dialog;
    loader.value = newValue.buttonLoader;
    console.log('watcher dialog >>>> ', newValue)
    if (newValue.card) {
      cardObject.value.platform = newValue.card.platform_name;
      cardObject.value.username = newValue.card.account_name;
      cardObject.value.password = newValue.card.password;
      cardObject.value['password_id'] = newValue.card.password_id;
    }
  },
  { immediate: true }
);

function closeDialog() {
  emit("close-dialog", false);
}
const AddNewAccount = () => {
  console.log("addnewAccount==");
  loader.value = true;
  emit("add-new-account", { cardObj: cardObject.value, key: false, loader: loader.value });
};
const updateAccount = (id) => {
  console.log("updateAccount==");
  loader.value = true;
  emit("update-account", { cardId: id, cardObj: cardObject.value, key: false, loader: loader.value });
};
</script>

<style scoped>
:deep .v-field__field:focus-within {
  background-color: #e0e0e0 !important;
}
</style>
