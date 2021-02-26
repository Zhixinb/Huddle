<template>
     <v-list-item @click="logout">
        <v-list-item-title>Logout</v-list-item-title>
    </v-list-item>
</template>

<script>
import { Auth } from 'aws-amplify';
import dbHelper from '../../db'

export default {
    methods: {
        async logout() {
            try {
                await Auth.signOut();
                dbHelper.logMetric("LogoutBtn")
                this.$router.push({ name: 'Login'})                
            } catch (error) {
                alert(error.message);
            }
        },
    },
    destroyed() {
        // this.$store.getters.uid === null
        // TODO: full clear store to default value instead of value by value
        this.$store.commit('set_uid', null)
    }
}
</script>

<style>

</style>