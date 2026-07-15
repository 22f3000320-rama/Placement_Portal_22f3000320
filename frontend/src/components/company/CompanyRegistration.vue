<template>
    <div class="container min-vh-100 d-flex justify-content-center align-items-center py-5">
        <div class="card shadow-lg border-0" style="max-width: 600px; width: 100%;">
            <div class="card-body p-5">
                <h2 class="text-center mb-4">Company Registration</h2>
                <form @submit.prevent="handleCompanyRegistration">
                    <div class="mb-3">
                        <label class="form-label" fw-semibold for="name">Name:</label>
                        <input type="text" class="form-control shadow-sm" id="name" v-model="form.name" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label" fw-semibold for="email">Email:</label>
                        <input type="email" class="form-control shadow-sm" id="email" v-model="form.email" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label" fw-semibold for="password">Password:</label>
                        <input type="password" class="form-control shadow-sm" id="password" v-model="form.password"
                            required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label" fw-semibold for="description">Description:</label>
                        <input type="text" class="form-control shadow-sm" id="description" v-model="form.description"
                            required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label" fw-semibold for="website">Website:</label>
                        <input type="text" class="form-control shadow-sm" id="website" v-model="form.website" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label" fw-semibold for="contact">Contact Number:</label>
                        <input type="tel" class="form-control shadow-sm" id="contact" maxlength="10" v-model="form.contact" required>
                    </div>
                    <div class="text-center mt-4">
                        <button class="btn btn-outline-success" type="submit">Register</button>
                    </div>
                </form>
                <div class="text-center mt-1">
                    <RouterLink :to="{ name: 'company-login' }">
                        Already have an account? Login here
                    </RouterLink>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import axios from 'axios';
    export default {
        name: 'CompanyRegistration',
        data() {
            return {
                form: {
                    name: '',
                    email: '',
                    password: '',
                    description: '',
                    website: '',
                    contact: ''
                }
            }
        },
        methods: {
            async handleCompanyRegistration() {
                try {
                    console.log(this.form);
                    const response = await axios.post('http://localhost:5000/api/company/register', this.form);
                    alert('Registration successful! You will be able to access the dashboard after approval from admin.');
                    this.$router.replace({
                        name: "company-login"
                    })
                } catch (error) {
                    if (error.response.data) {
                        console.error('Registration failed:', error.response.data);
                        alert('Registration failed. Please try again.');
                    }
                }
            }
        }
    }
</script>