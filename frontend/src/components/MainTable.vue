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
    <div v-for="(item, index) in cards" :key="index" class="d-flex">
      <Card
        :card="item"
        @delete-card="deleteAccount"
        @update-card="updateAccount"
      />
    </div>
  </div>
</template>

<script>
import Card from "../components/cards/index.vue";
import Dialog from "../components/dialog/index.vue";
import { ref } from "vue";
import API from "../services/API";
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
    const cards = ref([
      {
        platform_name: 'Google',
        account_name: 'ahmad2@gmail.com',
        password: 'wertyuvbnm567',
        password_id: '1',
      },
      {
        platform_name: 'Google',
        account_name: 'test@gmail.com',
        password: 'wertyuvbnm000',
        password_id: '2',
      },
      {
        platform_name: 'Github',
        account_name: 'test10@gmail.com',
        password: 'ikdyuvbnm520',
        password_id: '3'
      },
      {
        platform_name: 'Facebook',
        account_name: 'test@gmail.com',
        password: 'wertyuvbnm567',
        password_id: '4'
      },
      {
        platform_name: 'Google',
        account_name: 'test000@gmail.com',
        password: '7h8yuvbnm56hl',
        password_id: '5'
      },
      {
        platform_name: 'Google',
        account_name: 'test011@gmail.com',
        password: '7h8yuvbnm56hl',
        password_id: '6'
      },
      {
        platform_name: 'Google',
        account_name: 'test007@gmail.com',
        password: '7h8yuvbnm087l',
        password_id: '7'
      },
      {
        platform_name: 'Google',
        account_name: 'test8@gmail.com',
        password: '7h8yuvbnm56hl',
        password_id: '8'
      },
      {
        platform_name: 'Google',
        account_name: 'test5@gmail.com',
        password: '7h8yuvbnm56hl',
        password_id: '9'
      },
      {
        platform_name: 'Google',
        account_name: 'test1@gmail.com',
        password: '7h8yuvbnhhihl',
        password_id: '10'
      },
    ]);
    const loader = ref(true);
    const route = useRoute();
    const router = useRouter();
    const dialog = ref(false);
    const add = ref("add");
    const buttonLoader = ref(false)

    const getAllAccounts = () => {
      API.get("get_all_passwords")
        .then((res) => {
          // assign data to cards Array
          cards.value = res.passwords
        })
        .catch(() => {
          // show error message
          useToast(error?.message ? error.message : "Something went wrong", "error");
        })
        .finally(() => {
          loader.value = false;
        });
    };

    function deleteAccount(object) {
      console.log("deleted object ===", object);
      getAllAccounts();
      useToast("Account deleted successfully", "success");
    }

    const addNewAccount = (payload) => {
      API.post(`create_password`, payload.cardObj)
        .then((res) => {
          console.log("added new object ===", res);
          // add in cards Array,, state updated here
          getAllAccounts();
          useToast(res.message, "success");
        })
        .catch((err) => {
          // show error message
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