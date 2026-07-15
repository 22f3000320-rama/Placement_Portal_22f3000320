<template>
    <div class="container min-vh-100 d-flex justify-content-center align-items-center py-5">
        <div class="card shadow-lg border-0" style="max-width: 700px; width: 100%;">
            <div class="card-body p-5">
                <h2 class="text-center mb-4">Create New Drive</h2>
                <form @submit.prevent="createNewDrive">
                    <div class="mb-3">
                        <label class="form-label fw-semibold" for="title">Title:</label>
                        <input type="text" class="form-control shadow-sm" id="title" v-model="form.title" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-semibold" for="description">Description:</label>
                        <textarea class="form-control shadow-sm" rows="4" id="description" v-model="form.description"
                            required>
                        </textarea>
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
                        <label class="form-label fw-semibold" for="year">Graduation Year:</label>
                        <input type="number" class="form-control shadow-sm" id="year" v-model="form.year" required>
                    </div>
                    <div class="mb-3">
                        <label for="skills">Skills:</label>
                        <SkillSelector v-model="form.skills" :editable="true" />
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-semibold" for="cgpa_threshold">CGPA:</label>
                        <input type="number" class="form-control shadow-sm" id="cgpa_threshold" min="0" max="10"
                            step="0.01" v-model="form.cgpa_threshold" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-semibold" for="ctc">CTC (in LPA):</label>
                        <input type="number" class="form-control shadow-sm" id="ctc" step="0.1" min="0"
                            v-model="form.ctc" required>
                    </div>
                    <div class="mb-3">
                        <label class="form-label fw-semibold" for="ctc">Deadline:</label>
                        <input type="date" class="form-control shadow-sm" id="deadline" :min="today"
                            v-model="form.deadline" required>
                    </div>
                    <div class="text-center mt-4">
                        <button class="btn btn-outline-success me-2" type="submit">Submit for Approval</button>
                        <button class="btn btn-outline-success" @click="this.$router.back()">Close</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>
<script>
    import axios from 'axios';
    import SkillSelector from "../../components/common/SkillSelector.vue";
    export default {
        name: 'CreateDrive',
        components: {
            SkillSelector
        },
        data() {
            return {
                today: new Date().toISOString().split("T")[0],
                form: {
                    title: '',
                    description: '',
                    department: '',
                    ctc: null,
                    cgpa_threshold: null,
                    year: null,
                    skills: [],
                    deadline: ''
                }
            }
        },
        methods: {
            async createNewDrive() {
                const token = localStorage.getItem('access_token');
                try {
                    await axios.post('http://localhost:5000/api/company/post-drive', this.form,
                        {
                            headers: {
                                Authorization: `Bearer ${token}`
                            }
                        }
                    );
                    alert('Drive submitted to the admin for the approval.');
                    this.$router.push({ name: "company-ongoing-drives" });
                } catch (error) {
                    console.error('Error during drive creation:', error);
                    alert('Drive creation failed. Please try again.');
                }
            }
        }
    }
</script>