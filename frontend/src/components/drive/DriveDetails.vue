<template>
    <div class="container min-vh-100 d-flex justify-content-center align-items-center py-5">
        <div class="row justify-content-center w-100">
            <div class="col-12 d-flex justify-content-center">
                <div class="card shadow-sm rounded-3 w-100 text-break" style="max-width: 600px; min-height: 500px;">
                    <div v-if="isLoading" class="text-center my-5 d-flex flex-column justify-content-center h-100">
                        <p class="mt-2 text-muted">Fetching Drive Details...</p>
                    </div>
                    <div v-else-if="!drive" class="alert alert-warning shadow-sm" role="alert">
                        No Ongoing Drives.
                    </div>
                    <div v-else class="card-body p-5">
                        <div class="d-flex justify-content-between align-items-start">
                            <div>
                                <h2 class="card-title mb-5">
                                    Drive Details
                                </h2>
                                <p class="mb-0">
                                    <strong>Job Title:</strong> {{ drive.title }}
                                </p>
                                <p class="mb-3">
                                    <span v-if="role === 'admin' || role === 'company'">
                                        <strong>Drive ID:</strong> {{ drive.drive_id }}
                                    </span>

                                    <br v-if="role === 'admin'">

                                    <span v-if="role === 'admin' || role === 'student'">
                                        <strong>Company:</strong> {{ drive.company_name }}
                                    </span>
                                </p>
                            </div>
                            <div class="rounded-circle bg-primary text-white
                    d-flex justify-content-center align-items-center" style="width: 60px; height: 60px;">
                                {{ drive.company_name.charAt(0).toUpperCase() }}
                            </div>

                        </div>
                        <div class="mt-3">

                            <p class="mb-2">
                                <strong>Job Description:</strong> {{ drive.description }}
                            </p>
                            <p class="mb-2">
                                <strong>Eligible Branch:</strong> {{ drive.branch }}
                            </p>
                            <p class="mb-2">
                                <strong>Graduation Year:</strong> {{ drive.year_threshold }}
                            </p>
                            <p class="mb-2">
                                <strong>CGPA:</strong> {{ drive.cgpa_threshold }}
                            </p>
                            <p class="card-text">
                                <strong> Required Skills:</strong> {{ drive.skills.join(', ') }}
                            </p>
                            <p class="mb-2">
                                <strong>CTC (in LPA):</strong> {{ drive.ctc }}
                            </p>
                            <p class="mb-4">
                                <strong>Deadline:</strong> {{ drive.deadline }}
                            </p>
                        </div>
                        <div class="d-flex gap-2 justify-content-center">
                            <button v-if="role === 'student'" :disabled="drive.has_applied"
                                class="btn btn-outline-success btn-sm me-2 mt-4" @click="applyDrive(drive.drive_id)">{{
                                drive.has_applied ? 'Already Applied' :
                                'Apply Now' }}</button>
                            <button class="btn btn-outline-primary mt-4" @click="this.$router.back()">Close</button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import axios from 'axios';
    export default {
        name: 'DriveDetails',
        props: {
            role: {
                type: String,
                required: true
            }
        },
        data() {
            return {
                drive: null,
                isLoading:true,
            }
        },
        methods: {
            async fetchDriveDetails() {
                try {
                    const token = localStorage.getItem('access_token');

                    const res = await axios.get(
                        `http://localhost:5000/api/get-drive-details/${this.$route.params.driveId}`,
                        {
                            headers: {
                                Authorization: `Bearer ${token}`
                            }
                        }
                    );
                    this.drive = res.data.drive;
                }
                catch (error) {
                    alert(error.response.data.message);
                } finally {
                    this.isLoading = false;
                }
            },
            async applyDrive(driveId) {
                try {
                    const token = localStorage.getItem('access_token');
                    const res = await axios.post(`http://localhost:5000/api/student/apply-drive/${driveId}`, {},
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
                    alert("Failed to apply to the drive. Please try again.");
                }
            },
        },
        mounted() {
            this.fetchDriveDetails();
        }
    }
</script>