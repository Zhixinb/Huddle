<template>
  <div class="container">
    <form @submit.prevent="register">
        <h2>Register</h2>
        <v-text-field
        label="Email"
        :rules="[rules.required, rules.email]"
        v-model="email"
        outlined
        ></v-text-field>
        
        <v-text-field
            v-model="password"
            :append-icon="show ? 'mdi-eye' : 'mdi-eye-off'"
            :rules="[rules.required, rules.min]"
            :type="show ? 'text' : 'password'"
            label="Password"
            hint="At least 8 characters"
            counter
            outlined
            @click:append="show = !show"
          ></v-text-field>
        
        <v-btn
            block
            color="primary"
            large
            type="submit">Register</v-btn>        
    </form>
</div>
</template>

<script>
import { Auth } from 'aws-amplify';

export default {
    name: 'SignUpForm',
    data() { 
        return { 
            email: '', 
            password: '', 
            show: false,
            rules: {
            required: value => !!value || 'Required.',
            min: v => v.length >= 8 || 'Min 8 characters',
            email: value => {
                const pattern = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
                return pattern.test(value) || 'Invalid e-mail.'
                },
            },
        }; 
    },    
    methods: {
        async register() {
            try {
                await Auth.signUp({
                    username: this.email,
                    password: this.password,
                });
                alert('Please check your email for a verification link.');
            } catch (error) {
                alert(error.message);
            }
        }
    }
}
</script>

<style>

</style>