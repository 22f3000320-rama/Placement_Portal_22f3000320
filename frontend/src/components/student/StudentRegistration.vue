<template>
    <div class="container min-vh-100 d-flex justify-content-center align-items-center py-5">
        <div class="card shadow-lg border-0" style="max-width: 600px; width: 100%;">
            <div class="card-body p-5">
                <h2 class="text-center mb-4">Student Registration</h2>
                <form @submit.prevent="handleStudentRegistration">
                    <div class="mb-3">
                        <label class="form-label fw-semibold" for="name">Name:</label>
                        <input type="text" class="form-control shadow-sm" id="name" v-model="form.name" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-semibold" for="email">Email:</label>
                        <input type="email" class="form-control shadow-sm" id="email" v-model="form.email" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-semibold" for="password">Password:</label>
                        <input type="password" class="form-control shadow-sm" id="password" v-model="form.password"
                            required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-semibold" for="department">Department:</label>
                        <select class="form-select shadow-sm" id="department" v-model="form.department" required>
                            <option value="" disabled>Select your department...</option>
                            <option value="Computer Science (CSE)">Computer Science (CSE)</option>
                            <option value="Information Tech (IT)">Information Tech (IT)</option>
                            <option value="Electronics (ECE)">Electronics (ECE)</option>
                            <option value="Electrical (EE)">Electrical (EE)</option>
                            <option value="Mechanical (MECH)">Mechanical (MECH)</option>
                            <option value="Civil (CIVIL)">Civil (CIVIL)</option>
                        </select>
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-semibold" for="cgpa">CGPA:</label>
                        <input type="number" class="form-control shadow-sm" id="cgpa" v-model="form.cgpa" step="0.01"
                            min="0" max="10" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-semibold" for="year">Graduation Year:</label>
                        <input type="number" class="form-control shadow-sm" id="year" v-model="form.year" required>
                    </div>
                    <div class="mb-3">
                        <label for="skills">Skills:</label>
                        <SkillSelector v-model="form.skills" :editable="true" />
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-semibold" for="contact">Contact Number:</label>
                        <input type="tel" class="form-control shadow-sm" id="contact" maxlength="10"
                            v-model="form.contact" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-semibold" for="resume">Resume:</label>
                        <input type="file" accept=".pdf,.doc,.docx" class="form-control shadow-sm" id="resume"
                            v-on:change="onResumeChange" required>
                    </div>
                    <div class="text-center mt-4">
                        <button class="btn btn-outline-success" type="submit">Register</button>
                    </div>

                </form>
                <div class="text-center mt-1">
                    <RouterLink :to="{name:'student-login'}">
                        Already have an account? Login here
                    </RouterLink>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import axios from 'axios';
    import SkillSelector from "../../components/common/SkillSelector.vue";
    export default {
        name: 'StudentRegistration',
        components: {
            SkillSelector
        },
        data() {
            return {
                form: {
                    name: '',
                    email: '',
                    password: '',
                    department: '',
                    cgpa: null,
                    year: null,
                    skills: [],
                    contact: '',
                    resume: null
                }
            }
        },
        methods: {
            async handleStudentRegistration() {
                try {
                    await axios.post('http://localhost:5000/api/student/register', this.form);
                    alert('Registration successful! Please login to access your dashboard.');
                    this.$router.replace({ name: "student-login" });
                } catch (error) {
                    console.error('Error during registration:', error);
                    alert('Registration failed. Please try again.');
                }
            },
            onResumeChange() { }
        }
    }
</script>