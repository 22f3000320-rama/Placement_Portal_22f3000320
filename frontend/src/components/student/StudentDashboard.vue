<template>
    <div class="container mt-4">
        <header class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="mb-0">Welcome {{ name }}!</h2>

            <div>
                <RouterLink :to="{ name: 'student-profile', params: { studentId: studentId } }"
                    class="text-decoration-none me-2">
                    Edit Profile
                </RouterLink>

                <span class="mx-1">|</span>

                <RouterLink :to="{ name:'student-application-history', params: { studentId: studentId } }" class="text-decoration-none mx-2">
                    History
                </RouterLink>

                <span class="mx-1">|</span>

                <button class="btn btn-link text-danger text-decoration-none p-0 mx-2 align-baseline"
                    @click="logout()">Logout</button>

            </div>
        </header>

        <ul class="nav nav-tabs">
            <li class="nav-item">
                <RouterLink :to="{name:'student-companies'}" class="nav-link" active-class="active">
                    View Companies
                </RouterLink>
            </li>

            <li class="nav-item">
                <RouterLink :to="{ name:'student-applications' }" class="nav-link" active-class="active">
                    Your Applications
                </RouterLink>
            </li>

            <li class="nav-item">
                <RouterLink :to="{ name:'student-search' }" class="nav-link" active-class="active">
                    Search for:
                </RouterLink>
            </li>
        </ul>

        <div class="mt-4">
            <router-view v-slot="{Component}">
                <component :is="Component" role="student" />
            </router-view>
        </div>
    </div>
</template>

<script>
    export default {
        name: "StudentDashboard",
        data() {
            return {
                name: localStorage.getItem("name"),
                studentId: localStorage.getItem("studentId")
            }
        },
        methods: {
            logout() {
                localStorage.removeItem("access_token");
                localStorage.removeItem("name");
                localStorage.removeItem("studentId")
                this.$router.replace({ name: "student-login" });
            }
        },
        mounted() {
            if (!this.studentId){
                this.logout();
            }
        }
    };
</script>