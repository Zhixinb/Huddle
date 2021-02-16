<template>
     <v-list-item @click="logout">
        <v-list-item-title>Logout</v-list-item-title>
    </v-list-item>
</template>

<script>
import { Auth } from 'aws-amplify';

export default {
    methods: {
        async logout() {
            try {
                await Auth.signOut();
                // this.$store.getters.uid === null
                // TODO: full clear store to default value instead of value by value
                this.$store.commit('set_uid', null)
                this.$router.push({ name: 'Login'})
            } catch (error) {
                alert(error.message);
            }
        },
    },
}
</script>

<style>

</style>