<template>
    <div class="container mt-4">
        <div class="row justify-content-center">
            <div class="col-md-8 col-lg-9 mt-4">
                <div v-if="isLoading" class="text-center my-5">
                    <p class="mt-2 text-muted">Fetching Closed Drives...</p>
                </div>
                <div v-else-if="closedDrives.length == 0" class="alert alert-warning shadow-sm" role="alert">
                    No Closed Drives.
                </div>
                <div v-else>
                    <h2 class="mb-3">Closed Drives</h2>
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th scope="col">Sr no.</th>
                                    <th scope="col">Drive ID</th>
                                    <th scope="col">Title</th>
                                    <th v-if="role === 'admin'">Company</th>
                                    <th class="d-flex justify-content-end" scope="col">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(drive,index) in closedDrives" :key="drive.drive_id">
                                    <td>{{ index+1 }}</td>
                                    <td>Drive {{ drive.drive_id }}</td>
                                    <td>{{ drive.title }}</td>
                                    <td v-if="role === 'admin'">{{ drive.company_name }}</td>
                                    <td class="d-flex justify-content-end"><button
                                            class="btn btn-outline-primary btn-sm"
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
        name: 'ClosedDrives',
        props: {
            role: {
                type: String,
                required: true
            }
        },
        data() {
            return {
                closedDrives: [],
                isLoading: true,
            }
        },
        methods: {
            async fetchClosedDrives() {
                try {
                    const token = localStorage.getItem('access_token');
                    const res = await axios.get('http://localhost:5000/api/get-closed-drives', {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    })

                    this.closedDrives = res.data.closedDrives;
                }

                catch (error) {
                    console.error('Failed to fetch closed drives.', error);
                    this.closedDrives = [];
                } finally{
                    this.isLoading=false;
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
            this.fetchClosedDrives();
        }
    }
</script>