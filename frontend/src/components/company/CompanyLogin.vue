<template>
    <div class="container min-vh-100 d-flex justify-content-center align-items-center py-5">
        <div class="card shadow-lg border-0" style="max-width: 600px; width: 100%;">
            <div class="card-body p-5">
                <h2 class="text-center mb-4">Company Login</h2>
                <form @submit.prevent="handleLogin">
                    <div class="mb-3">
                        <label class="form-label" fw-semibold for="email">Email:</label>
                        <input type="email" class="form-control shadow-sm" id="email" v-model="form.email" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label" fw-semibold for="password">Password:</label>
                        <input type="password" class="form-control shadow-sm" id="password" v-model="form.password"
                            required>
                    </div>
                    <div class="text-center mt-4">
                        <button class="btn btn-outline-success" type="submit">Login</button>
                    </div>
                </form>
                <div class="text-center mt-1">
                    <RouterLink :to="{ name: 'company-register' }">
                        Don't have an account? Register here
                    </RouterLink>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    export default {
        name: 'CompanyLogin',
        data() {
            return {
                form: {
                    email: '',
                    password: ''
                }
            }
        },
        methods: {
            async handleLogin() {
                try {
                    const response = await axios.post('http://localhost:5000/api/company/login', this.form);
                    localStorage.setItem('access_token', response.data.access_token);
                    localStorage.setItem('name', response.data.data.name);
                    this.$router.replace({
                        name: "company-ongoing-drives"
                    })
                } catch (error) {
                    if (error.response) {
                        alert(error.response.data.message);
                        this.form.email = '';
                        this.form.password = '';
                    }
                }
            }
        }
    }
</script>