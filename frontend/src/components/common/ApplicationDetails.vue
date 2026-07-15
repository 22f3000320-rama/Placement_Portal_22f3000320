<template>
    <div class="container mt-4">
        <div class="row justify-content-center">
            <div class="col-lg-6">
                <div class="card shadow-sm rounded-3">
                    <div v-if="isLoading" class="text-center my-5">
                        <p class="mt-2 text-muted">Fetching Application Details...</p>
                    </div>
                    <div v-else-if="!application" class="alert alert-danger shadow-sm" role="alert">
                        Application Details NOT FOUND.
                    </div>
                    <div v-else class="card-body p-4">
                        <div class="d-flex justify-content-between align-items-start">
                            <div>
                                <h4 class="card-title mb-1">
                                    Application Details
                                </h4>
                            </div>
                            <div class="rounded-circle bg-primary text-white
                    d-flex justify-content-center align-items-center" style="width: 60px; height: 60px;">
                                {{ application.student_name.charAt(0).toUpperCase() }}
                            </div>
                        </div>
                        <div class="mt-3">
                            <p>
                                <strong>Student Name:</strong> {{ application.student_name }}
                            </p>
                            <p class="mb-2">
                                <strong>Department:</strong> {{ application.student_department }}
                            </p>
                            <p class="mb-2">
                                <strong>Student CGPA:</strong> {{ application.student_cgpa }}
                            </p>
                            <p class="mb-2">
                                <strong>Drive ID:</strong> {{ application.drive_id }}
                            </p>
                            <p class="mb-2">
                                <strong>Job Title:</strong> {{ application.drive_title }}
                            </p>
                            <p class="mb-2">
                                <strong>Contact:</strong> {{ application.student_contact }}
                            </p>
                        </div>
                        <div v-if="role === 'company'" class="card mt-4">
                            <div class="card-body">
                                <h5 class="card-title">Update Candidate Status</h5>
                                <p class="text-muted">Current status: {{ application.status }}</p>
                                <div v-if="application.status!='Rejected'" class="d-flex align-items-center mt-3">
                                    <select class="form-select me-3" v-model="updateForm.status"
                                        style="max-width: 250px;">
                                        <option value="" disabled>Select decision...</option>
                                        <option value="Selected">Selected</option>
                                        <option value="Rejected">Rejected</option>
                                        <option value="Pending">Under Review</option>
                                    </select>

                                    <button class="btn btn-outline-success btn-sm"
                                        @click="saveCandidateStatus(application.application_id)"
                                        :disabled="!updateForm.status">
                                        Save changes
                                    </button>
                                </div>

                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="text-center mt-4">
                <button class="btn btn-outline-success" @click="this.$router.back()">Close</button>
            </div>
        </div>
    </div>
</template>
<script>
    import axios from 'axios';
    export default {
        name: 'ApplicationDetails',
        props: {
            role: {
                type: String,
                required: true
            }
        },
        data() {
            return {
                application: null,
                updateForm: {
                    status: ""
                },
                isLoading: true,
            }
        },
        methods: {
            async fetchApplicationDetails() {
                try {
                    const token = localStorage.getItem('access_token');

                    const res = await axios.get(
                        `http://localhost:5000/api/get-application-details/${this.$route.params.applicationId}`,
                        {
                            headers: {
                                Authorization: `Bearer ${token}`
                            }
                        }
                    );
                    this.application = res.data.application;
                } catch (error) {
                    alert(error.response.data.message);
                } finally {
                    this.isLoading = false;
                }
            },
            async saveCandidateStatus(applicationId) {
                try {
                    const token = localStorage.getItem('access_token');
                    const res = await axios.patch(`http://localhost:5000/api/company/save-application-status/${applicationId}`,
                        this.updateForm,
                        {
                            headers: {
                                Authorization: `Bearer ${token}`
                            }
                        }
                    );
                    alert(res.data.message);
                    this.fetchApplicationDetails();
                }
                catch (error) {
                    console.log("Failed to update application status.")
                    alert(error.response.data.message);
                }
            }
        },
        mounted() {
            this.fetchApplicationDetails();
        }
    }
</script>