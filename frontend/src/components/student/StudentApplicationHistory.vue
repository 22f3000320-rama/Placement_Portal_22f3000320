<template>
    <div class="container mt-4">
        <div class="row justify-content-center">
            <div class="col-md-8 col-lg-6 mt-4">
                <div v-if="isLoading" class="text-center my-5">
                    <p class="mt-2 text-muted">Fetching Your Application History...</p>
                </div>
                <div v-else-if="applications.length == 0" class="alert alert-warning shadow-sm" role="alert">
                    No Student Applications found.
                </div>
                <div v-else>
                    <h2 class="mb-3">Student Application History</h2>
                    <div class="text-primary">
                        <h5 class="mb-2">Student Name: {{ applications[0].student_name }}</h5>
                        <h5 class="mb-2">Student ID: {{ applications[0].student_id }}</h5>
                        <h5 class="mb-2">Department: {{ applications[0].student_department }}</h5>
                    </div>
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th scope="col">Sr no.</th>
                                    <th scope="col">Drive ID</th>
                                    <th scope="col">Job Title</th>
                                    <th scope="col">Company</th>
                                    <th scope="col">Results</th>
                                </tr>
                            </thead>
                            <tbody v-if="applications.length > 0">
                                <tr v-for="(application,index) in applications" :key="application.application_id">
                                    <td>{{ index+1 }}</td>
                                    <td>{{ application.drive_id }}</td>
                                    <td>{{ application.title }}</td>
                                    <td>{{ application.company_name }}</td>
                                    <td><strong>{{ application.status }}</strong></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="d-flex justify-content-center mt-4">
                        <button v-if="role==='student'" class="btn btn-outline-primary me-2" @click="triggerExport()">Export Application
                            History</button>
                        <button class="btn btn-outline-primary" @click="this.$router.back()">Close</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import axios from 'axios';
    export default {
        name: 'StudentApplicationHistory',
        props: {
            role: {
                type: String,
                required: true
            }
        },
        data() {
            return {
                applications: [],
                isLoading: true,
            }
        },
        methods: {
            async fetchApplicationHistory() {
                try {
                    const token = localStorage.getItem('access_token');
                    const studentId = this.$route.params.studentId || localStorage.getItem('studentId');
                    console.log("The Student ID being sent is:", studentId);

                    const res = await axios.get(`http://localhost:5000/api/get-student-application-history/${studentId}`,
                        {
                            headers: {
                                'Authorization': `Bearer ${token}`
                            }
                        }
                    );
                    this.applications = res.data.applications;
                } catch (error) {
                    console.error('Failed to fetch history.', error);
                    this.applications = [];
                } finally {
                    this.isLoading = false;
                }
            },
            async triggerExport() {
                const token = localStorage.getItem('access_token');
                try {
                    const res = await axios.get(`http://localhost:5000/api/student/export-application-history`,
                        {
                            headers: {
                                Authorization: `Bearer ${token}`
                            }
                        }
                    );
                    alert(res.data.message);
                }
                catch (error) {
                    alert('Failed to export!');
                    console.error('Export Failed.', error);
                }
            },
        },
        mounted() {
            this.fetchApplicationHistory();
        }
    }
</script>