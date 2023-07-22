<template>
  <Dialog
    :dialog="dialog"
    :dialogKey="add"
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
  <div v-for="(item, index) in cards" :key="index" class="d-flex">
    <Card
      :card="item"
      @delete-card="deleteAccount"
      @update-card="updateAccount"
    />
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
    const cards = ref([1, 2, 3, 4, 5, 6, 7, 8, 9, 0]);
    const loader = ref(true);
    const route = useRoute();
    const router = useRouter();
    const dialog = ref(false);
    const add = ref("add");

    const getAllAccounts = () => {
      API.get("get_all_password")
        .then((res) => {
          // assign data to cards array
          // cards.value = res.data
        })
        .catch(() => {
          // show error message
          useToast("Something went wrong", "error");
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
      API.post(`create_password`, payload.cardObject)
        .then((res) => {
          console.log("added new object ===", object);
          // console.log('res.data added new === ', res.data)
          // add in cards array
          getAllAccounts();
          useToast("Account added successfully", "success");
        })
        .catch((err) => {
          // show error message
          useToast(error, "error");
        })
        .finally(() => {
          dialog.value = payload.key;
        });
    };

    function updateAccount(object) {
      console.log("updated object ===", object);
      getAllAccounts();
      useToast("Account updated successfully", "success");
    }

    onMounted(() => {
      getAllAccounts();
    });

    return {
      loader,
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
