<template>
    <div class="container mt-4">
        <header class="d-flex justify-content-between align-items-center mb-4">
            <h1 class="mb-0">Welcome Admin</h1>
            <button class="btn btn-outline-danger" @click="logout()">Logout</button>
        </header>
        <div class="container mt-4">
            <ul class="nav nav-tabs">
                <li class="nav-item">
                    <RouterLink class="nav-link" active-class="active"
                        :to="{name:'admin-companies'}">Manage Companies</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink class="nav-link" active-class="active"
                         :to="{name:'admin-students'}">Manage Students</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink class="nav-link" active-class="active"
                        :to="{name:'admin-company-applications'}">Company Applications</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink class="nav-link" active-class="active"
                        :to="{name:'admin-pending-drives'}">Pending Drives</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink class="nav-link" active-class="active"
                        :to="{name:'admin-ongoing-drives'}">Ongoing Drives</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink class="nav-link" active-class="active"
                          :to="{name:'admin-student-applications'}">Student Applications</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink class="nav-link" active-class="active" 
                        :to="{ name: 'admin-rejected-drives' }">Rejected Drives</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink class="nav-link" active-class="active"
                        :to="{name:'admin-closed-drives'}">Closed Drives</RouterLink>
                </li>
                <li class="nav-item">
                    <RouterLink class="nav-link" active-class="active"
                        :to="{name:'admin-search'}">Search for:</RouterLink>
                </li>
            </ul>
            <div class="mt-4">
                <router-view v-slot="{Component}">
                    <component :is="Component" role="admin"/>
                </router-view>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: 'AdminDashboard',
        methods: {
            logout() {
                
                localStorage.removeItem('access_token');
                this.$router.replace({name: 'admin-login'});
            }
        }
    }
</script>