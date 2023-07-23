<template>
  <Dialog
    :dialog="dialog"
    :dialogKey="add"
    :buttonLoader="buttonLoader"
    @close-dialog="dialog = false"
    @add-new-account="addNewAccount"
  />
  <div class="mt-13 text-right mr-5">
    <v-btn
      variant="text"
      color="deep-orange"
      class="text-capitalize"
      @click="dialog = true"
    >
      <v-icon icon="mdi-plus"></v-icon>
      add new account
    </v-btn>
  </div>
  <div
    v-if="loader"
    class="d-flex justify-center align-center"
    style="height:65vh">
    <v-progress-circular
      indeterminate
      size="50"
      color="deep-orange"
    ></v-progress-circular>
  </div>
  <div v-else>
    <div
      v-if="!cards.length"
      class="txt32 font-weight-medium"
      style="height:60vh">
      <div class="not-found ">
        Data not exists 
      </div>
    </div>
    <div v-else>
      <div v-for="(item, index) in cards" :key="index" class="d-flex">
        <Card
          :card="item"
          @delete-card="deleteAccount"
          @update-card="updateAccount"
        />
      </div>
    </div>
  </div>
</template>

<script>
import Card from "../components/cards/index.vue";
import Dialog from "../components/dialog/index.vue";
import { ref } from "vue";
import API from "../services/API";
import axios from "axios";
import { useRoute } from "vue-router";
import { useRouter } from "vue-router";
import useToast from "@/plugins/useToast.js";
import { onMounted } from "vue";
export default {
  components: {
    Card,
    Dialog
  },
  setup() {
    const cards = ref([])
    const loader = ref(true);
    const route = useRoute();
    const router = useRouter();
    const dialog = ref(false);
    const add = ref("add");
    const buttonLoader = ref(false)

    const getAllAccounts = () => {
      const token = JSON.parse(localStorage.getItem('token'))
      const appBaseURL = import.meta.env.VITE_API_URL

        let config = {
          method: 'get',
          maxBodyLength: Infinity,
          url: `${appBaseURL}get_all_passwords`,
          headers: { 
            'Content-Type': 'application/json', 
            'Authorization': `Bearer ${token}`,
          },
        };

        axios.request(config)
        .then((response) => {
          console.log(JSON.stringify(response));
          cards.value = response.data.passwords
        })
        .catch((error) => {
          console.log(error);
          useToast(error?.message ? error.message : "Something went wrong", "error");
        })
        .finally(() => {
          loader.value = false
      });
    };

    function deleteAccount(object) {
      console.log("deleted object ===", object);
      getAllAccounts();
      useToast("Account deleted successfully", "success");
    }

    const addNewAccount = (payload) => {
      console.log('get update payload >>>', payload.cardObj)
      let data = JSON.stringify(payload.cardObj);
      const token = JSON.parse(localStorage.getItem('token'))
      const appBaseURL = import.meta.env.VITE_API_URL

        let config = {
          method: 'post',
          maxBodyLength: Infinity,
          url: `${appBaseURL}create_password`,
          headers: { 
            'Content-Type': 'application/json', 
            'Authorization': `Bearer ${token}`,
          },
          data : data
        };

        axios.request(config)
        .then((response) => {
          console.log(JSON.stringify(response));
          getAllAccounts();
          useToast(res.message, "success");
        })
        .catch((error) => {
          console.log(error);
          useToast(err?.message ? err?.message : "New account did not add", "error");
        })
        .finally(() => {
          dialog.value = payload.key;
          buttonLoader.value = false
      });
    };

    function updateAccount(object) {
      console.log("updated object ====", object);
      getAllAccounts();
      useToast("Account updated successfully", "success");  
    }

    onMounted(() => {
      setTimeout(() => {
        loader.value = false
      }, 1000);
      getAllAccounts();
    });

    return {
      loader,
      buttonLoader,
      cards,
      add,
      dialog,
      route,
      router,
      getAllAccounts,
      deleteAccount,
      addNewAccount,
      updateAccount
    };
  },

  methods: {},
};
</script>
<style scoped>
.not-found {
  position: absolute;
  top: 50%; right: 50%;
  transform: translate(50%,-50%)
}
</style>