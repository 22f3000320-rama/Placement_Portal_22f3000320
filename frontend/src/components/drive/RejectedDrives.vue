<template>
    <div class="container mt-4">
        <div class="row justify-content-center">
            <div class="col-md-8 col-lg-6 mt-4">
                <div v-if="isLoading" class="text-center my-5">
                    <p class="mt-2 text-muted">Fetching Rejected Drives...</p>
                </div>
                <div v-else-if="rejectedDrives.length == 0" class="alert alert-warning shadow-sm" role="alert">
                    No Rejected Drives.
                </div>
                <div v-else>
                    <h2 class="mb-3">Rejected Drives</h2>
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th scope="col">Sr no.</th>
                                    <th scope="col">Drive ID</th>
                                    <th scope="col">Title</th>
                                    <th v-if="role === 'admin'">Company</th>
                                    <th scope="col">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(drive,index) in rejectedDrives" :key="drive.drive_id">
                                    <td>{{ index+1 }}</td>
                                    <td>Drive {{ drive.drive_id }}</td>
                                    <td>{{ drive.title }}</td>
                                    <td v-if="role === 'admin'">{{ drive.company_name }}</td>
                                    <td><button class="btn btn-outline-primary btn-sm"
                                            @click="viewDrive(drive.drive_id)">View Drive</button>
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
        name: 'RejectedDrives',
        props: {
            role: {
                type: String,
                required: true
            }
        },
        data() {
            return {
                rejectedDrives: [],
                isLoading : true,
            }
        },
        methods: {
            async fetchRejectedDrives() {
                try {
                    const token = localStorage.getItem('access_token');
                    const res = await axios.get('http://localhost:5000/api/get-rejected-drives', {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    })

                    this.rejectedDrives = res.data.rejectedDrives;
                } catch (error) {
                    console.error('Failed to fetch rejected drives.', error);
                    this.rejectedDrives = [];
                } finally{
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
        },
        mounted() {
            this.fetchRejectedDrives();
        }
    }
</script>