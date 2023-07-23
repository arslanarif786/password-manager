<template>
  <Dialog
    :dialog="dialog"
    :card="card"
    :dialogKey="edit"
    :buttonLoader="buttonLoader"
    @close-dialog="dialog = false"
    @update-account="updateAccount"
  />
  <DeleteAccount
    :dialog="deleteRowDialog"
    :card="card"
    :buttonLoader="buttonLoader"
    @close-delete-popup="deleteRowDialog = false"
    @handle-delete="deleteAccount"
  />
  <div class="w-100">
    <v-card style="width: 90%" height="70" class="mx-auto my-3">
      <div class="d-flex align-center pt-2 px-5">
        <span class="icon-chip">
          <img :src="google" alt="" style="height: 100%" />
        </span>
        <div class="mx-10" style="width:80px">{{ card.platform }}</div>
        <div class="mx-10" style="width:170px">{{ card.username }}</div>
        <v-text-field
          hide-details
          flat
          readonly
          :value="card.password"
          :type="password.visible ? 'text' : password.type"
          :append-inner-icon="password.visible ? 'mdi-eye-off' : 'mdi-eye'"
          @click:append-inner="password.visible = !password.visible"
          variant="solo"
        />
        <v-icon
          icon="mdi-pencil"
          color="grey-darken-1"
          class="ml-1 mr-3 cursor-pointer"
          @click="dialog = true"
        ></v-icon>
        <v-icon
          icon="mdi-delete"
          color="red"
          class="cursor-pointer"
          @click="deleteRowDialog = true"
          outlined
        ></v-icon>
      </div>
    </v-card>
  </div>
</template>

<script>
import { ref } from "vue";
import Dialog from "../dialog/index.vue";
import DeleteAccount from "../DeleteCard.vue";
import google from "@/assets/images/google.png";
import API from "@/services/API";
import useToast from "@/plugins/useToast.js";

export default {
  components: {
    Dialog,
    DeleteAccount,
  },
  props: ["card"],
  setup(props, { emit }) {
    const dialog = ref(false);
    const deleteRowDialog = ref(false);
    const edit = ref("edit");
    const buttonLoader = ref(false)
    const password = ref({
      model: "",
      type: "password",
      visible: false,
    });
    function deleteAccount(object) {
      console.log('delete payload id >>>', object.cardId)

      API.delete(`delete_password/${object.cardId}`)
        .then((res) => {
          // update cards array after deletion
          emit("delete-card", object.cardId);
        })
        .catch((err) => {
          // show error message
          useToast(err.message, "error");
        })
        .finally(() => {
          deleteRowDialog.value = object.key;
          buttonLoader.value = false
        });
    }

    const updateAccount = (payload) => {
      console.log('get update payload >>>', payload)

      API.put(`update_password/${payload.cardId}`, payload.cardObject)
        .then((res) => {
          // update cards array
          emit("update-card", payload);
        })
        .catch((err) => {
          // show error message
          useToast(error, "error");
        })
        .finally(() => {
          dialog.value = payload.key;
          buttonLoader.value = false
        });
    };
    return {
      dialog,
      buttonLoader,
      deleteRowDialog,
      edit,
      password,
      google,
      deleteAccount,
      updateAccount,
    };
  },
};
</script>

<style scoped>
:deep .v-input__control {
  width: 300px;
  background-color: #fbefeb;
  border-radius: 30px;
}
/* :deep .v-field__input {
  color: orangered;
} */
</style>
