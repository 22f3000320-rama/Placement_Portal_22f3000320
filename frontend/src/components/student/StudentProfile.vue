<template>
    <div class="container min-vh-100 d-flex justify-content-center align items-center py-5">
        <div class="card shadow-lg border-0" style="max-width: 600px; width: 100%;">
            <div v-if="student" class="card-body p-5">
                <h3 class="text-center mb-4">Update Profile Details</h3>
                <form @submit.prevent="updateProfile(student.student_id)">
                    <div class="mb-3">
                        <label class="form-label fw-semibold" for="name">Name:</label>
                        <input type="text" class="form-control shadow-sm" id="name" v-model="student.name" disabled>
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-semibold" for="name">Department:</label>
                        <input type="text" class="form-control shadow-sm" id="name" v-model="student.department"
                            disabled>
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-semibold" for="cgpa">CGPA:</label>
                        <input type="number" class="form-control shadow-sm" id="cgpa" v-model="form.cgpa" step=0.1
                            required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-semibold" for="year">Year:</label>
                        <input type="number" class="form-control shadow-sm" id="year" v-model="form.year" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-semibold" for="skills">Skills:</label>
                        <SkillSelector v-model="form.skills" :editable="true" />
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-semibold" for="contact">Contact:</label>
                        <input type="tel" class="form-control shadow-sm" id="contact" v-model="form.contact" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-semibold" for="resume_file">Resume:</label>
                        <input type="file" class="form-control shadow-sm" id="resume_file" accept=".pdf,.doc,.docx">
                    </div>
                    <div class="text-center mt-4">
                        <button type="submit" class="btn btn-outline-success btn-sm me-2">Save Profile</button>
                    </div>
                </form>
                <div class="text-end mt-2">
                    <button class="btn btn-outline-success btn-sm" @click="this.$router.back()">Close</button>
                </div>
            </div>
            <div v-else class="text-center py-5">
                <p>Loading profile...</p>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import SkillSelector from "../../components/common/SkillSelector.vue";

    export default {
        name: 'StudentProfile',
        components: {
            SkillSelector
        },
        data() {
            return {
                student: null,
                form: {
                    cgpa: null,
                    year: null,
                    contact: '',
                    skills: []
                }
            }
        },
        methods: {
            async fetchStudentDetails() {
                try {
                    const token = localStorage.getItem('access_token');
                    const res = await axios.get(
                        `http://localhost:5000/api/get-student-details/${this.$route.params.studentId}`,
                        {
                            headers: {
                                Authorization: `Bearer ${token}`
                            }
                        }
                    );
                    this.student = res.data.student;
                    this.form.cgpa = this.student.cgpa;
                    this.form.year = this.student.year;
                    this.form.contact = this.student.contact;
                    this.form.skills = [...this.student.skills];
                } catch (error) {
                    console.error('Failed to fetch student:', error);
                    alert(error.response.data.message);
                }
            },
            async updateProfile(studentId) {
                try {
                    const token = localStorage.getItem('access_token');
                    const res = await axios.put(`http://localhost:5000/api/student/update-profile/${studentId}`, this.form,
                        {
                            headers: {
                                Authorization: `Bearer ${token}`
                            }
                        }
                    );
                    alert(res.data.message);
                    this.$router.back();
                } catch (error) {
                    alert(error.response.data.message);
                    alert("Failed to update profile details. Please try again.");
                }
            },
        },
        mounted() {
            this.fetchStudentDetails();
        }
    }
</script>