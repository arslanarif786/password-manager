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
  
  <!-- For Desktop Web Screen -->
  <div v-if="$vuetify.display.mdAndUp" class="w-100">
    <v-card style="width: 90%" height="70" class="mx-auto my-3">
      <div class="d-flex align-center pt-2 px-5">
        <span class="icon-chip">
          <img :src="google" alt="" style="height: 100%" />
        </span>
        <div class="mx-10 font-weight-bold" style="width: 80px">
          {{ card.platform_name }}
        </div>
        <div class="mx-10" style="width: 170px">{{ card.account_name }}</div>
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

  <!-- For Tablet and Mobile Screen -->
  <div v-else class="w-100 px-10">
    <v-card class="mx-auto my-3">
      <div class="d-flex justify-space-between">
        <div class="d-flex">
          <span class="icon-chip mt-7 mx-4">
            <img :src="google" alt="" style="height: 100%" />
          </span>
          <div class="pt-3" :class="$vuetify.display.sm ? 'ml-2' : ''">
            <div class="font-weight-bold">{{ card.platform_name }}</div>
            <div class="">{{ card.account_name }}</div>
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
          </div>
        </div>
        <div class="d-flex" :class="$vuetify.display.smAndUp ? 'mt-11' : 'mt-3'">
          <v-icon
            icon="mdi-pencil"
            color="grey-darken-1"
            class="cursor-pointer"
            :class="$vuetify.display.smAndUp ? 'mr-3' : 'mr-1'"
            @click="dialog = true"
          ></v-icon>
          <v-icon
            icon="mdi-delete"
            color="red"
            class="mr-4 cursor-pointer"
            @click="deleteRowDialog = true"
            outlined
          ></v-icon>
        </div>
      </div>
    </v-card>
  </div>
</template>

<script>
import { ref } from "vue";
import Dialog from "../dialog/index.vue";
import axios from "axios";
import DeleteAccount from "../DeleteCard.vue";
import google from "@/assets/images/google.png";
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

      const token = JSON.parse(localStorage.getItem('token'))
      const appBaseURL = import.meta.env.VITE_API_URL

        let config = {
          method: 'delete',
          maxBodyLength: Infinity,
          url: `${appBaseURL}delete_password/?password_id=${object.cardId}`,
          headers: { 
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`,

          },
          data : payload
        };

        axios.request(config)
        .then((res) => {
          if(res.message == 'Password entry deleted successfully')
          {
            // update cards array after deletion
            emit("delete-card", object.cardId);
          }
          else {
            console.log(res);
            useToast(res.message, "error");
          }
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

    function updateAccount(payload) {
      console.log('get update payload >>>', payload.cardObj)
      let data = JSON.stringify(payload.cardObj);
      const token = JSON.parse(localStorage.getItem('token'))
      const appBaseURL = import.meta.env.VITE_API_URL

        let config = {
          method: 'put',
          maxBodyLength: Infinity,
          url: `${appBaseURL}update_password/?password_id=${payload.cardId}`,
          headers: { 
            'Content-Type': 'application/json', 
            'Authorization': `Bearer ${token}`,
          },
          data : data
        };

        axios.request(config)
        .then((response) => {
          console.log(JSON.stringify(response.data));
          if(response.message == 'Password entry updated successfully')
          {
            emit("update-card", payload)
          }
          else {
            console.log(response);
            useToast(response.message, "error");
          }
        })
        .catch((error) => {
          console.log(error);
          useToast(error.message, "error");
        })
        .finally(() => {
          dialog.value = payload.key;
          buttonLoader.value = false
      });

    }
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
@media screen and (min-width: 959px) {
  :deep .v-input__control {
    width: 300px;
  }
}
/* :deep .v-field__input {
  color: orangered;
} */

@media screen and (max-width: 959px) {
  :deep .v-field__input {
    padding-inline-start: 0;
    padding-inline-end: 0;
    padding-top: 0;
    height: 40px;
  }
  :deep .v-input__control {
    width: 200px;
  }
  :deep .v-field__append-inner {
    align-items: unset;
    padding-top: 10px;
  }
}
</style>
