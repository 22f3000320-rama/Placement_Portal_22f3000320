<template>
    <div class="container mt-4">
        <header class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="mb-0">Welcome {{ name }}!</h2>
            <button class="btn btn-outline-danger" @click="logout()">Logout</button>
        </header>
        <div class="container mt-4">
            <ul class="nav nav-tabs">
                <li class="nav-item">
                    <RouterLink class="nav-link" active-class="active" :to="{ name: 'company-ongoing-drives' }">Ongoing
                        Drives</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink class="nav-link" active-class="active" :to="{ name: 'company-pending-drives' }">Pending
                        Drives</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink class="nav-link" active-class="active" :to="{ name: 'company-rejected-drives' }">
                        Rejected
                        Drives</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink class="nav-link" active-class="active" :to="{ name: 'company-closed-drives' }">Closed
                        Drives</RouterLink>
                </li>
            </ul>
            <div class="mt-4">
                <router-view v-slot="{ Component }">
                    <component :is="Component" role="company" />
                </router-view>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'CompanyDashboard',
    data() {
        return {
            name: ""
        }
    },
    methods: {
        logout() {
            localStorage.removeItem('access_token');
            localStorage.removeItem("name");
            this.$router.replace({ name: 'company-login' });
        }
    },
    mounted() {
        this.name = localStorage.getItem("name");
    }
}
</script>