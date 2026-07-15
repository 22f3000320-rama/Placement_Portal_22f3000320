<template>
    <div class="container mt-4">
        <div class="card shadow-sm rounded-3">
            <div class="card-body p-4">
                <h5 class="card-title mb-4">What are you looking for?</h5>

                <div class="d-flex align-items-center mb-4">
                    <select class="form-select" v-model="searchFor" @change="resetFilters" style="max-width: 250px;">
                        <option value="" disabled>Select an option...</option>
                        <option value="Companies">Companies</option>
                        <option value="Drives">All Drives (Filter manually)</option>
                        <option v-if="role === 'student'" value="EligibleDrives">Eligible Drives</option>
                        <option v-if="role === 'admin'" value="Students">Students</option>
                    </select>
                </div>

                <div v-if="searchFor === 'Companies'" key="path-companies">
                    <div class="mb-3">
                        <label class="form-label">Select a Company:</label>
                        <select class="form-select" v-model="filters.companyId" style="max-width: 300px;">
                            <option value="null" disabled>Choose a company...</option>
                            <option v-for="company in companyList" :key="company.value" :value="company.value">
                                {{ company.text }}
                            </option>
                        </select>
                    </div>
                    <button class="btn btn-primary mt-3" :disabled="!filters.companyId"
                        @click="viewCompany(filters.companyId)">
                        View Details
                    </button>
                </div>

                <div v-else-if="searchFor === 'Drives'" key="path-drives">
                    <div class="row">
                        <div class="col-md-5 mb-3">
                            <label class="form-label d-block fw-bold">Graduation Year</label>
                            <div class="form-check form-check-inline" v-for="year in yearOptions" :key="year.value">
                                <input class="form-check-input" type="radio" :name="'gradYear'"
                                    :id="'year_' + year.value" :value="year.value" v-model="filters.gradYear">
                                <label class="form-check-label" :for="'year_' + year.value">{{ year.text }}</label>
                            </div>
                        </div>

                        <div class="col-md-3 mb-3">
                            <label class="form-label fw-bold">Min CGPA</label>
                            <input type="number" class="form-control" v-model="filters.cgpa" step="0.1"
                                placeholder="e.g. 7.5">
                        </div>

                        <div class="col-md-4 mb-3">
                            <label class="form-label fw-bold">Department</label>
                            <select class="form-select" v-model="filters.department">
                                <option value="null" disabled>Select Branch</option>
                                <option v-for="dept in deptOptions" :key="dept.value" :value="dept.value">
                                    {{ dept.text }}
                                </option>
                            </select>
                        </div>

                        <div class="col-md-4 mb-3">
                            <label class="form-label fw-bold">Skills:</label>
                            <SkillSelector v-model="filters.skills" :editable="true" />
                        </div>
                    </div>
                    <div class="text-center mt-4">
                        <button class="btn btn-primary mt-3" @click="viewDrives">View Drives</button>
                    </div>
                </div>

                <div v-else-if="searchFor === 'EligibleDrives'" key="path-eligible">
                    <div class="alert alert-info mt-2" role="alert">
                        We will automatically find drives matching your profile.
                    </div>
                    <button class="btn btn-success mt-2" @click="eligibleDrives">View Eligible Drives</button>
                </div>

                <div v-else-if="searchFor === 'Students' && role === 'admin'" key="path-students">
                    <div class="row">
                        <div class="col-md-5 mb-3">
                            <label class="form-label d-block fw-bold">Graduation Year</label>
                            <div class="form-check form-check-inline" v-for="year in yearOptions" :key="year.value">
                                <input class="form-check-input" type="radio" :name="'studentGradYear'"
                                    :id="'student_year_' + year.value" :value="year.value" v-model="filters.gradYear">
                                <label class="form-check-label" :for="'student_year_' + year.value">{{ year.text
                                    }}</label>
                            </div>
                        </div>


                        <div class="col-md-3 mb-3">
                            <label class="form-label fw-bold">Min CGPA</label>
                            <input type="number" class="form-control" v-model="filters.cgpa" step="0.1" min="0" max="10"
                                placeholder="e.g. 7.5">
                        </div>

                        <div class="col-md-4 mb-3">
                            <label class="form-label fw-bold">Department</label>
                            <select class="form-select" v-model="filters.department">
                                <option value="null" disabled>Select Branch</option>
                                <option v-for="dept in deptOptions" :key="dept.value" :value="dept.value">
                                    {{ dept.text }}
                                </option>
                            </select>
                        </div>

                        <div class="col-md-4 mb-3">
                            <label class="form-label fw-bold">Skills:</label>
                            <SkillSelector v-model="filters.skills" :editable="true" />
                        </div>
                    </div>
                    <button class="btn btn-primary mt-3" @click="viewStudents">Search Students</button>
                </div>
                <div class="text-center mt-4">
                    <button class="btn btn-outline-success" @click="this.$router.back()">Close</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import SkillSelector from "../common/SkillSelector.vue";
    export default {
        name: 'Search',
        components: { SkillSelector },
        props: {
            role: {
                type: String,
                required: true
            }
        },
        data() {
            return {
                searchFor: '',
                filters: {
                    companyId: null,
                    gradYear: null,
                    cgpa: null,
                    department: null,
                    skills: []
                },
                companyList: [],
                yearOptions: [
                    { value: 2022, text: '2022' }, { value: 2023, text: '2023' },
                    { value: 2024, text: '2024' }, { value: 2025, text: '2025' },
                    { value: 2026, text: '2026' }, { value: 2027, text: '2027' },
                    { value: 2028, text: '2028' }
                ],
                deptOptions: [
                    { value: 'Computer Science (CSE)', text: 'Computer Science (CSE)' },
                    { value: 'Information Tech (IT)', text: 'Information Tech (IT)' },
                    { value: 'Electronics (ECE)', text: 'Electronics (ECE)' },
                    { value: 'Electrical (EE)', text: 'Electrical (EE)' },
                    { value: 'Mechanical (MECH)', text: 'Mechanical (MECH)' },
                    { value: 'Civil (CIVIL)', text: 'Civil (CIVIL)' }
                ]
            }
        },
        methods: {
            async fetchCompanies() {
                try {
                    const token = localStorage.getItem('access_token');
                    const res = await axios.get('http://localhost:5000/api/get-companies', {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    })
                    this.companyList = res.data.companies.map(company => ({
                        value: company.company_id,
                        text: company.name
                    }));
                    console.log(res.data.companies)
                } catch (error) {
                    console.error('Failed to fetch companies.');
                    this.companyList = [];
                    this.skills = []
                }
            },
            resetFilters() {
                this.filters = { companyId: null, gradYear: null, cgpa: null, department: null, skills: [] };
            },
            viewCompany(companyId) {
                if (this.role === 'admin') {
                    this.$router.push({
                        name: "admin-company-details",
                        params: {
                            companyId: companyId
                        }
                    });
                } else {
                    this.$router.push({
                        name: "student-company-details",
                        params: {
                            companyId: companyId
                        }
                    });
                }
            },
            viewDrives() {
                const queryParams = {};
                if (this.filters.gradYear) queryParams.gradYear = this.filters.gradYear;
                if (this.filters.cgpa) queryParams.cgpa = this.filters.cgpa;
                if (this.filters.department) queryParams.department = this.filters.department;
                if (this.filters.skills) queryParams.skills = this.filters.skills.toString();

                if (this.role === 'admin') {
                    this.$router.push({
                        name: "admin-search-drives",
                        query: queryParams
                    });
                } else {
                    this.$router.push({
                        name: "student-search-drives",
                        query: queryParams
                    });
                }
            },
            eligibleDrives() {
                this.$router.push({
                    name: 'student-search-drives',
                    query: { type: 'eligible' }
                });
            },
            viewStudents() {
                const queryParams = {};
                if (this.filters.gradYear) queryParams.gradYear = this.filters.gradYear;
                if (this.filters.cgpa) queryParams.cgpa = this.filters.cgpa;
                if (this.filters.department) queryParams.department = this.filters.department;
                if (this.filters.skills) queryParams.skills = this.filters.skills.toString();

                this.$router.push({
                    name: "admin-search-students",
                    query: queryParams
                });
            },
        },
        mounted() {
            this.fetchCompanies();
        }
    }
</script>