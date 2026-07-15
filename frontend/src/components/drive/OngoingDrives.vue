<template>
    <div class="container mt-4">
        <div class="row justify-content-center">
            <div class="col-md-8 col-lg-9 mt-4">
                <div v-if="isLoading" class="text-center my-5">
                    <p class="mt-2 text-muted">Fetching Ongoing Drives...</p>
                </div>
                <div v-else-if="ongoingDrives.length == 0" class="alert alert-warning shadow-sm" role="alert">
                    No Ongoing Drives.
                </div>
                <div v-else>
                    <header class="d-flex justify-content-between align-items-center mb-4">
                        <h2 class="mb-0">Ongoing Drives</h2>
                        <span v-if="role==='admin'" class="badge bg-success px-3 py-2">{{ driveCount }}</span>
                        <button v-if="role === 'company'" class="btn btn-outline-primary" @click="createDrive()">
                            <i class="bi bi-plus-lg me-1"></i>Create New
                        </button>
                    </header>
                    <div class="table-responsive">
                        <table class="table table-striped">
                            <thead>
                                <tr>
                                    <th scope="col">Sr no.</th>
                                    <th scope="col">Drive ID</th>
                                    <th scope="col">Title</th>
                                    <th v-if="role === 'admin'">Company</th>
                                    <th class="d-flex justify-content-center" scope="col">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(drive,index) in ongoingDrives" :key="drive.drive_id">
                                    <td>{{ index+1 }}</td>
                                    <td>Drive {{ drive.drive_id }}</td>
                                    <td>{{ drive.title }}</td>
                                    <td v-if="role === 'admin'">{{ drive.company_name }}</td>
                                    <td class="d-flex justify-content-end"><button
                                            class="btn btn-outline-primary btn-sm me-2"
                                            @click="viewDrive(drive.drive_id)">View</button>
                                        <button v-if="role === 'company'" class="btn btn-outline-primary btn-sm me-2"
                                            @click="viewApplications(drive.drive_id)">Applications</button>
                                        <button class="btn btn-outline-danger btn-sm"
                                            @click="closeDrive(drive.drive_id)">
                                            Mark as Closed
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
        name: 'OngoingDrives',
        props: {
            role: {
                type: String,
                required: true
            }
        },
        data() {
            return {
                ongoingDrives: [],
                isLoading : true,
                driveCount:null,
            }
        },
        methods: {
            async fetchOngoingDrives() {
                try {
                    const token = localStorage.getItem('access_token');
                    const res = await axios.get('http://localhost:5000/api/get-ongoing-drives', {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    })
                    this.driveCount = res.data.driveCount;
                    this.ongoingDrives = res.data.ongoingDrives;
                } catch (error) {
                    console.error('Failed to fetch ongoing drives.', error);
                    this.ongoingDrives = [];
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
            viewApplications(driveId) {
                this.$router.push({
                    name: "company-drive-applications",
                    params: {
                        driveId: driveId
                    }
                });
            },
            createDrive() {
                this.$router.push({
                    name: "company-create-drive"
                })
            },
            async closeDrive(driveId) {
                const token = localStorage.getItem('access_token');
                try {
                    const res = await axios.patch(`http://localhost:5000/api/close-drive/${driveId}`, {},
                        {
                            headers: {
                                Authorization: `Bearer ${token}`
                            }
                        }
                    );
                    alert(res.data.message);
                    this.fetchOngoingDrives();
                }
                catch (error) {
                    alert(error.response.data.message);
                }
            }
        },
        mounted() {
            this.fetchOngoingDrives();
        }
    }
</script>