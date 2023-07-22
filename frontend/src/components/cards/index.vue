<template>
  <Dialog
    :dialog="dialog"
    :card="card"
    :dialogKey="edit"
    @close-dialog="dialog = false"
    @update-account="updateAccount"
  />
  <DeleteAccount
    :dialog="deleteRowDialog"
    :card="card"
    @close-delete-popup="deleteRowDialog = false"
    @handle-delete="deleteAccount"
  />
  <div class="w-100">
    <v-card style="width: 90%" height="70" class="mx-auto my-3">
      <div class="d-flex align-center pt-2 px-5">
        <span class="icon-chip">
          <img :src="fb" alt="" style="height: 100%" />
        </span>
        <div class="mx-10">App Title</div>
        <div class="mx-10">testdannyganza@canada.com</div>
        <!-- readonly -->
        <v-text-field
          hide-details
          flat
          v-model="password.model"
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
import fb from "@/assets/images/google.png";
import rules from "@/constants/validation-rules.js";
import API from "@/services/API";
import { useRouter } from "vue-router";
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
    const password = ref({
      model: "",
      type: "password",
      visible: false,
    });
    function deleteAccount(object) {
      API.delete(`delete_password/${object.cardId}`)
        .then((res) => {
          // console.log('res.data delete === ', res.data)
          // update cards array
          emit("delete-card", res);
        })
        .catch((err) => {
          // show error message
          useToast(error, "error");
        })
        .finally(() => {
          deleteRowDialog.value = object.key;
        });
    }

    const updateAccount = (payload) => {
      API.put(`update_password/${payload.cardId}`, payload.cardObject)
        .then((res) => {
          // console.log('res.data updated === ', res.data)
          // update cards array
          emit("update-card", res);
        })
        .catch((err) => {
          // show error message
          useToast(error, "error");
        })
        .finally(() => {
          dialog.value = payload.key;
        });
    };
    return {
      dialog,
      deleteRowDialog,
      edit,
      password,
      fb,
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
:deep .v-field__input {
  color: orangered;
}
</style>
