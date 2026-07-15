<template>
    <div class="container mt-4">
        <div class="row justify-content-center">
            <div class=" col-md-8 col-lg-9 mt-4">
                <div v-if="isLoading" class="text-center my-5">
                    <p class="mt-2 text-muted">Fetching Student Applications...</p>
                </div>
                <div v-else-if="studentApplications.length == 0" class="alert alert-warning shadow-sm" role="alert">
                    No Student Applications found.
                </div>
                <div v-else>
                    <h2 v-if="role === 'admin'" class="mb-3">Student Applications</h2>
                    <h2 v-if="role === 'student'" class="mb-3">Applied Drives</h2>
                    <h2 v-if="role === 'company'" class="mb-3">Received Applications</h2>
                    <p v-if="role === 'company' && studentApplications.length > 0" class="mb-3"><strong>Job Title:
                        </strong> {{ studentApplications[0].title }}</p>
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th scope="col">Sr no.</th>
                                    <th v-if="role === 'admin' || role === 'company'" scope="col">Student Name</th>
                                    <th v-if="role === 'admin' || role === 'student'" scope="col">Title</th>
                                    <th v-if="role === 'admin' || role === 'student'" scope="col">Company</th>
                                    <th scope="col">Date</th>
                                    <th class="d-flex justify-content-end" scope="col">Action</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(application,index) in studentApplications"
                                    :key="application.application_id">
                                    <td>{{ index+1 }}</td>
                                    <td v-if="role === 'admin' || role === 'company'" scope="col">{{
                                        application.student_name }}</td>
                                    <td v-if="role === 'admin' || role === 'student'" scope="col">{{ application.title
                                        }}</td>
                                    <td v-if="role === 'admin' || role === 'student'" scope="col">{{
                                        application.company_name }}</td>
                                    <td>{{ application.applied_at }}</td>
                                    <td class="d-flex justify-content-end">
                                        <button v-if="role === 'admin' || role === 'student'"
                                            class="btn btn-outline-primary btn-sm"
                                            @click="viewApplication(application.application_id)">View Details
                                        </button>
                                        <button v-if="role === 'company'" class="btn btn-outline-primary btn-sm"
                                            @click="viewApplication(application.application_id)">Review Application
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="text-center mt-4">
                        <button class="btn btn-outline-success" @click="this.$router.back()">Close</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import axios from 'axios';
    export default {
        name: 'StudentDriveApplications',
        props: {
            role: {
                type: String,
                required: true
            }
        },
        data() {
            return {
                driveId: null,
                studentApplications: [],
                isLoading: true,
            }
        },
        methods: {
            async fetchStudentApplications() {
                try {
                    const token = localStorage.getItem('access_token');
                    const config = {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        },
                        params: {}
                    };
                    if (this.role === 'company') {
                        config.params.driveId = this.driveId;
                    }
                    const res = await axios.get('http://localhost:5000/api/get-student-applications', config);
                    console.log(res.data)
                    this.studentApplications = res.data.studentApplications;
                } catch (error) {
                    console.error('Failed to fetch student applications.', error);
                    this.studentApplications = [];
                } finally {
                    this.isLoading = false;
                }
            },
            viewApplication(applicationId) {
                if (this.role === 'admin') {
                    this.$router.push({
                        name: "admin-application-details",
                        params: {
                            applicationId: applicationId
                        }
                    });
                } else if (this.role === 'company') {
                    this.$router.push({
                        name: "company-application-details",
                        params: {
                            applicationId: applicationId
                        }
                    });
                } else {
                    this.$router.push({
                        name: "student-application-details",
                        params: {
                            applicationId: applicationId
                        }
                    });
                }
            },
        },
        mounted() {
            this.driveId = this.$route.params.driveId;
            this.fetchStudentApplications();
        }
    }
</script>