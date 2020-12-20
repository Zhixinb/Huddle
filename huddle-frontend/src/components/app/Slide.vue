<template>
    <v-fade-transition appear>
        <div class="pa-2">
        <v-card width=100% height=150px>
            <div>
                {{ this.message }}
            </div>
        </v-card>
        </div>
    </v-fade-transition>
</template>

<script>
export default {
    name: 'slide',
    props: ['message']
}
</script>
