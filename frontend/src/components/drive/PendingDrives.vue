<template>
    <div class="container mt-4">
        <div class="row justify-content-center">
            <div class="col-md-8 col-lg-6 mt-4">
                <div v-if="isLoading" class="text-center my-5">
                    <p class="mt-2 text-muted">Fetching Pending Drives...</p>
                </div>
                <div v-else-if="pendingDrives.length == 0" class="alert alert-warning shadow-sm" role="alert">
                    No Pending Drives.
                </div>
                <div v-else>
                    <h2 class="mb-3">Pending Drives</h2>
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th scope="col">Sr no.</th>
                                    <th scope="col">Drive ID</th>
                                    <th scope="col">Title</th>
                                    <th v-if="role === 'admin'" scope="col">Company</th>
                                    <th class="d-flex justify-content-center" scope="col">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(drive,index) in pendingDrives" :key="drive.drive_id">
                                    <td>{{ index+1 }}</td>
                                    <td>Drive {{ drive.drive_id }}</td>
                                    <td>{{ drive.title }}</td>
                                    <td v-if="role === 'admin'">{{ drive.company_name }}</td>
                                    <td class="d-flex justify-content-end"><button
                                            class="btn btn-outline-primary btn-sm me-2"
                                            @click="viewDrive(drive.drive_id)">View Drive</button>
                                        <button v-if="role==='admin'" class="btn btn-outline-success btn-sm me-2"
                                            @click="approveDrive(drive.drive_id)">Approve</button>
                                        <button v-if="role==='admin'" class="btn btn-outline-danger btn-sm"
                                            @click="rejectDrive(drive.drive_id)">Reject
                                        </button>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
    import axios from 'axios';
    export default {
        name: 'PendingDrives',
        props: {
            role: {
                type: String,
                required: true
            }
        },
        data() {
            return {
                pendingDrives: [],
                isLoading: true,
            }
        },
        methods: {
            async fetchPendingDrives() {
                try {
                    const token = localStorage.getItem('access_token');
                    const res = await axios.get('http://localhost:5000/api/get-pending-drives', {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    })

                    this.pendingDrives = res.data.pendingDrives;
                    console.log(res.data.pendingDrives)
                } catch (error) {
                    console.error('Failed to fetch pending drives.', error);
                    this.pendingDrives = [];
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
                        name: "company-drive-details",
                        params: {
                            driveId: driveId
                        }
                    });
                }
            },
            async approveDrive(driveId) {
                try {
                    const token = localStorage.getItem('access_token');

                    const res = await axios.patch(
                        `http://localhost:5000/api/admin/approve-drive/${driveId}`, {},
                        {
                            headers: {
                                Authorization: `Bearer ${token}`
                            }
                        }
                    );
                    alert(res.data.message);
                    this.fetchPendingDrives();
                }
                catch (error) {
                    alert(error.response.data.message);
                }
            },
            async rejectDrive(driveId) {
                try {
                    const token = localStorage.getItem('access_token');

                    const res = await axios.patch(
                        `http://localhost:5000/api/admin/reject-drive/${driveId}`, {},
                        {
                            headers: {
                                Authorization: `Bearer ${token}`
                            }
                        }
                    );
                    alert(res.data.message);
                    this.fetchPendingDrives();
                }
                catch (error) {
                    alert(error.response.data.message);
                }
            }
        },
        mounted() {
            this.fetchPendingDrives();
        }
    }
</script>