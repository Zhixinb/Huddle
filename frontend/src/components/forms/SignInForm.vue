<template>
  <div class="container">
    <form @submit.prevent="login">
        <h2>Login</h2>

        <v-text-field
        label="Email"
        :rules="[rules.required]"
        v-model="email"
        outlined
        ></v-text-field>

        <v-text-field
            v-model="password"
            :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
            :rules="[rules.required]"
            :type="show ? 'text' : 'password'"
            label="Password"
            outlined
            @click:append="show = !show"
          ></v-text-field>
        
        <v-btn
            block
            color="primary"
            large
            type="submit">Login</v-btn>   
    </form>
</div>
</template>

<script>
import { Auth } from 'aws-amplify';

export default {
    name: "SignInForm",
    data() {
        return {
            email: '',
            password: '',
            show: false,
            rules: {
            required: value => !!value || 'Required.',    
            }       
        }
    },
    methods: {
        async login() {
            try {
                await Auth.signIn(this.email, this.password);
                
                await this.redirectToHome();
            } catch (error) {
                alert(error.message);
            }
        },
        async redirectToHome() {
            await Auth.currentUserInfo().then(data => {
                    console.log(data)
                    if (data && data.attributes) {
                        this.$store.commit('set_email', data.attributes.email)
                        // TODO: currently unable to get username from email or email from username
                        // thus unable to use username (uid) for adding permission, temp resolution is using
                        // email as uid
                        // this.$store.commit('set_uid', data.username)
                        this.$store.commit('set_uid', data.attributes.email)
                        this.$router.push({ name: 'Home'})
                    }
            })
        }
    },
    created() {
        if (this.$store.getters.uid !== null) { 
            this.redirectToHome();
        }
    }
}
</script>

<style>

</style>