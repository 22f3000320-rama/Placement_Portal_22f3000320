<template>
    <div class="container mt-4 min-vh-100">
        <div class="row justify-content-center">
            <div class="col-lg-6">
                <div class="card shadow-sm rounded-3">
                    <div v-if="isLoading" class="text-center my-5">
                        <p class="mt-2 text-muted">Fetching Company Details...</p>
                    </div>
                    <div v-else-if="!company" class="alert alert-danger shadow-sm" role="alert">
                        Company Not Found.
                    </div>
                    <div v-else class="card-body p-4">
                        <div class="d-flex justify-content-between align-items-start">
                            <div>
                                <h2 class="card-title mb-3">
                                    {{ company.name }}
                                </h2>
                                <p class="text-muted mb-1">
                                    {{ company.website }}
                                </p>
                                <p class="text-muted mb-1">
                                    {{ company.email }}
                                </p>

                            </div>
                            <div class="rounded-circle bg-primary text-white d-flex justify-content-center align-items-center"
                                style="width: 60px; height: 60px;">
                                {{ company.name.charAt(0).toUpperCase() }}
                            </div>

                        </div>
                        <h6 class="mt-4">Overview</h6>

                        <p class="card-text">
                            {{ company.description }}
                        </p>
                        <p class="card-text">
                            <strong>Contact:</strong> {{ company.contact }}
                        </p>
                        <h4 class="mt-4">Current Drives</h4>

                        <table class="table table-striped table-sm" v-if="company.company_drives.length > 0">
                            <thead>
                                <tr>
                                    <th>Sr No</th>
                                    <th>Drive Title</th>
                                    <th v-if="role==='admin'">Status</th>
                                    <th class="text-end">Actions</th>
                                </tr>
                            </thead>

                            <tbody>
                                <tr v-for="(drive, index) in company.company_drives" :key="drive.drive_id">
                                    <td>{{ index + 1 }}</td>
                                    <td>{{ drive.title }}</td>
                                    <td v-if="role==='admin'"><strong>{{ drive.status }}</strong></td>
                                    <td class="text-end"><button class="btn btn-outline-primary btn-sm"
                                            @click="viewDrive(drive.drive_id)">View Drive</button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                        <p v-else class="text-muted">
                            No active drives.
                        </p>
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
        name: 'CompanyDetails',
        props: {
            role: {
                type: String,
                required: true
            }
        },
        data() {
            return {
                company: null,
                isLoading: true,
            }
        },
        computed: {
            companyId() {
                return this.$route.params.companyId;
            }
        },
        methods: {
            async fetchCompanyDetails() {
                try {
                    const token = localStorage.getItem('access_token');
                    const res = await axios.get(
                        `http://localhost:5000/api/get-company-details/${this.companyId}`,
                        {
                            headers: {
                                Authorization: `Bearer ${token}`
                            }
                        }
                    );
                    console.log(res.data.company)
                    this.company = res.data.company;
                }
                catch (error) {
                    if (error.response) {
                        alert(error.response.data.message);
                    }
                } finally {
                    this.isLoading = false;
                }
            },
            viewDrive(driveId) {
                if (this.role === 'admin') {
                    this.$router.push({
                        name: "admin-drive-details",
                        params: {
                            driveId: driveId
                        }
                    });
                } else {
                    this.$router.push({
                        name: "student-drive-details",
                        params: {
                            driveId: driveId
                        }
                    });
                }
            },
        },
        mounted() {
            this.fetchCompanyDetails();
        }
    }
</script>